import os
import json
import logging
import time
import requests
from typing import List, Dict, Any, Optional
# from langchain_groq import ChatGroq  # Commented out - replaced with OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, ValidationError
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Suppress verbose HTTP request logs from OpenAI and httpx
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

class LLMAPIError(Exception):
    """Custom exception for LLM API errors."""
    pass

class LLMResponseError(Exception):
    """Custom exception for errors in LLM response structure or content."""
    pass

class LLMClient:
    def __init__(self, api_key: str = None, model_name: str = "gpt-4o", llm_instance: Optional[ChatOpenAI] = None):
        # def __init__(self, api_key: str = None, model_name: str = "llama3-70b-8192", llm_instance: Optional[ChatGroq] = None):  # Groq version
        if llm_instance:
            self.llm = llm_instance
            self.api_key = None  # Can't track costs without API key
        else:
            if not api_key:
                raise ValueError("API key must be provided if llm_instance is not given.")
            # self.llm = ChatGroq(api_key=api_key, model_name=model_name)  # Groq version
            self.llm = ChatOpenAI(api_key=api_key, model=model_name)
            self.api_key = api_key
        
        # Track session statistics
        self.session_start_time = int(time.time())
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def _track_token_usage(self, response) -> None:
        """Track token usage from LLM response."""
        try:
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                usage = response.usage_metadata
                self.prompt_tokens += usage.get('input_tokens', 0)
                self.completion_tokens += usage.get('output_tokens', 0)
                self.total_tokens += usage.get('total_tokens', 0)
            elif hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
                usage = response.response_metadata['token_usage']
                self.prompt_tokens += usage.get('prompt_tokens', 0)
                self.completion_tokens += usage.get('completion_tokens', 0) 
                self.total_tokens += usage.get('total_tokens', 0)
        except Exception as e:
            logging.debug(f"Could not track token usage: {e}")

    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics including token usage and estimated cost."""
        try:
            end_time = int(time.time())
            duration = (end_time - self.session_start_time) / 60
            
            # Estimate cost based on GPT-4o pricing (approximate)
            # Input: ~$0.005/1K tokens, Output: ~$0.015/1K tokens
            estimated_cost = (self.prompt_tokens * 0.005 / 1000) + (self.completion_tokens * 0.015 / 1000)
            
            return {
                "total_tokens": self.total_tokens,
                "prompt_tokens": self.prompt_tokens,
                "completion_tokens": self.completion_tokens,
                "estimated_cost": estimated_cost,
                "session_duration_minutes": duration,
                "start_time": self.session_start_time,
                "end_time": end_time
            }
        except Exception as e:
            return {"error": f"Error calculating session stats: {e}"}

    def get_session_costs(self) -> Dict[str, Any]:
        """Get current session costs from OpenAI API."""
        if not self.api_key:
            return {"error": "API key not available for cost tracking", "cost": 0.0}
        
        try:
            # Current time as end point
            end_time = int(time.time())
            
            # Query OpenAI costs API
            url = "https://api.openai.com/v1/organization/costs"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "start_time": self.session_start_time,
                "end_time": end_time,
                "bucket_width": "1d"  # Daily buckets
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Sum up costs from all buckets in the session timeframe
            total_cost = 0.0
            if "data" in data:
                for bucket in data["data"]:
                    total_cost += bucket.get("cost", 0.0)
            
            return {
                "session_cost": total_cost,
                "session_duration_minutes": (end_time - self.session_start_time) / 60,
                "start_time": self.session_start_time,
                "end_time": end_time
            }
            
        except requests.exceptions.RequestException as e:
            logging.warning(f"Could not fetch cost data from OpenAI: {e}")
            return {"error": f"API request failed: {e}", "cost": 0.0}
        except Exception as e:
            logging.warning(f"Error getting session costs: {e}")
            return {"error": f"Unexpected error: {e}", "cost": 0.0}

    def _load_prompt_from_file(self, file_name: str) -> str:
        file_path = os.path.join("prompts", file_name)
        if not os.path.exists(file_path):
            logging.error(f"Prompt file not found: {file_path}")
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def analyze_writing_style(self, text: str) -> Dict[str, Any]:
        """Analyzes the writing style of the given text."""
        try:
            prompt_template = self._load_prompt_from_file("analyze_style.md")
            prompt = ChatPromptTemplate.from_template(prompt_template)
            
            chain = prompt | self.llm
            response = chain.invoke({"text": text})
            
            # Track token usage
            self._track_token_usage(response)
            
            # The response may contain markdown ```json ... ``` or other text, so we need to handle that
            response_content = response.content
            logging.debug(f"Raw LLM response for style analysis: {response_content}")

            # Find the start and end of the JSON object
            start_index = response_content.find('{')
            end_index = response_content.rfind('}')

            if start_index != -1 and end_index != -1 and start_index < end_index:
                json_str = response_content[start_index:end_index+1]
            else:
                # If no JSON object is found, raise an error
                raise LLMResponseError("No valid JSON object found in the LLM response.")

            return json.loads(json_str)
        except FileNotFoundError:
            raise
        except json.JSONDecodeError as e:
            logging.error(f"LLM response validation error for writing style analysis: {e}")
            raise LLMResponseError(f"Invalid LLM response for writing style analysis: {e}")
        except RequestException as e:
            logging.error(f"LLM API request error during writing style analysis: {e}")
            raise LLMAPIError(f"LLM API error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during writing style analysis: {e}")
            raise

    def rate_pr_against_ksbs(self, pr_details: Dict[str, Any], ksb_list: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Rates a pull request against a list of KSBs."""
        try:
            prompt_template = self._load_prompt_from_file("rate_pr_against_ksbs.md")
            prompt = ChatPromptTemplate.from_template(prompt_template)

            ksb_formatted_list = "\n".join([f"{ksb['id']}: {ksb['description']}" for ksb in ksb_list])
            
            chain = prompt | self.llm.with_structured_output(KSBMatchList)
            response = chain.invoke({"ksb_list": ksb_formatted_list, **pr_details})
            
            # Track token usage (structured output doesn't have usage_metadata, estimate from content)
            # This is a workaround - structured output doesn't expose token usage directly
            estimated_tokens = len(str(response)) // 4  # Rough estimate: 4 chars per token
            self.total_tokens += estimated_tokens
            self.completion_tokens += estimated_tokens // 2
            self.prompt_tokens += estimated_tokens // 2
            
            # Explicitly validate the response to catch issues with structured output
            validated_response = KSBMatchList.model_validate(response.model_dump())
            return [match.model_dump() for match in validated_response.matches]
        except FileNotFoundError:
            raise
        except (ValidationError, json.JSONDecodeError) as e:
            logging.error(f"LLM response validation error for KSB rating: {e}")
            raise LLMResponseError(f"Invalid LLM response for KSB rating: {e}")
        except RequestException as e:
            logging.error(f"LLM API request error during KSB rating: {e}")
            raise LLMAPIError(f"LLM API error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during KSB rating: {e}")
            raise

    def rephrase_portfolio(self, portfolio_text: str, style_guide: Dict[str, Any]) -> str:
        """Rephrases the portfolio text based on a style guide."""
        try:
            prompt_template = self._load_prompt_from_file("refine_chapter_with_style_guide.md")
            prompt = ChatPromptTemplate.from_template(prompt_template)

            formatted_prompt = prompt.invoke({
                "tone": style_guide.get("tone", "professional"),
                "vocabulary_examples": ", ".join(style_guide.get("vocabulary_examples", [])),
                "sentence_structure": style_guide.get("sentence_structure", "varied"),
                "common_phrases": ", ".join(style_guide.get("common_phrases", [])),
                "draft_chapter": portfolio_text
            })
            response = self.llm.invoke(formatted_prompt)
            
            # Track token usage
            self._track_token_usage(response)
            
            return response.content
        except FileNotFoundError:
            raise
        except RequestException as e:
            logging.error(f"LLM API request error during portfolio rephrasing: {e}")
            raise LLMAPIError(f"LLM API error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during portfolio rephrasing: {e}")
            raise

    def generate_chapter_title(self, chapter_text: str) -> str:
        """Generates a title for a portfolio chapter."""
        try:
            prompt_template = self._load_prompt_from_file("generate_chapter_title.md")
            prompt = ChatPromptTemplate.from_template(prompt_template)

            chain = prompt | self.llm
            response = chain.invoke({"chapter_text": chapter_text})
            
            # Track token usage
            self._track_token_usage(response)
            
            return response.content
        except FileNotFoundError:
            raise
        except RequestException as e:
            logging.error(f"LLM API request error during chapter title generation: {e}")
            raise LLMAPIError(f"LLM API error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during chapter title generation: {e}")
            raise

class KSBMatch(BaseModel):
    ksb_id: str = Field(..., description="The ID of the KSB")
    score: int = Field(..., ge=0, le=100, description="Confidence score (0-100)")
    justification: str = Field(..., description="Justification for the score, explaining how the PR demonstrates the KSB.")

class KSBMatchList(BaseModel):
    matches: List[KSBMatch] = Field(..., description="List of KSB matches")

class WritingStyle(BaseModel):
    tone: str = Field(..., description="Overall tone of the writing (e.g., formal, informal, technical)")
    vocabulary_examples: List[str] = Field(..., description="Examples of frequently used or characteristic vocabulary")
    sentence_structure: str = Field(..., description="Description of typical sentence structure (e.g., complex, simple, varied)")
    common_phrases: List[str] = Field(..., description="Examples of common phrases or idioms used")
