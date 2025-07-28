import os
import json
import logging
from typing import List, Dict, Any, Optional
# from langchain_groq import ChatGroq  # Commented out - replaced with OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, ValidationError
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

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
        else:
            if not api_key:
                raise ValueError("API key must be provided if llm_instance is not given.")
            # self.llm = ChatGroq(api_key=api_key, model_name=model_name)  # Groq version
            self.llm = ChatOpenAI(api_key=api_key, model=model_name)

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
