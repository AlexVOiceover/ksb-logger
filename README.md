# KSB Logger

A CLI tool to generate a professional software development portfolio from GitHub Pull Requests (PRs) by assessing them against a set of Knowledge, Skills, and Behaviors (KSBs).

## Features

*   **Pull PRs**: Fetches pull requests for a given GitHub user from their public repositories. This can be modified to include private repositories by editing the `github_client.py` file and removing `?type=public` from the `get_user_public_repos` method. Note that accessing private repositories requires a GitHub Personal Access Token with appropriate permissions.
*   **Rate Work**: Assesses the fetched PRs against predefined KSBs using an LLM.
*   **Write Portfolio**: Generates a markdown-based portfolio, creating narrative chapters for each KSB based on the highest-rated PRs, ensuring the most impactful work is highlighted.

## Installation

1.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    ```

2.  **Activate the virtual environment**:
    ```bash
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **VS Code users**: Select the correct Python interpreter (`Cmd+Shift+P` → "Python: Select Interpreter" → choose `./venv/bin/python`) to resolve import warnings.

## Configuration

### Environment Variables

This tool requires specific environment variables to be configured. **You must create a `.env` file** in the project root with the following variables:

```env
# Required: GitHub Personal Access Token
GITHUB_API="your_github_token_here"

# Required: Your GitHub username for PR fetching
GITHUB_USERNAME="your_github_username"

# Required: OpenAI API key for LLM processing
OPENAI_API_KEY="your_openai_api_key_here"

# Optional: Can be removed as days_back functionality has been removed
# GITHUB_DAYSBACK=200

# Deprecated (commented out - replaced with OpenAI)
# GROQ_API="your_groq_api_key_here"
```

#### How to obtain the required tokens:

**GitHub Personal Access Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Select scopes: `repo` (for private repos) or `public_repo` (for public repos only)
4. Copy the generated token

**OpenAI API Key:**
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-proj-...`)

⚠️ **Security Note**: Never commit your `.env` file to version control. It's already ignored by `.gitignore`.

### Changing the LLM Provider

This project uses `langchain` for LLM integration, specifically `langchain_openai` and the `ChatOpenAI` model by default (migrated from Groq). To switch to a different LLM provider (e.g., Google Generative AI), you will need to:

1.  **Install the relevant Langchain package**: For example, for Google AI, `pip install langchain-google-genai`.
2.  **Modify `llm_client.py`**: Change the import statement from `from langchain_openai import ChatOpenAI` to the appropriate class (e.g., `from langchain_google_genai import ChatGoogleGenerativeAI`).
3.  **Update the `LLMClient` initialization**: In the `LLMClient`'s `__init__` method, change `self.llm = ChatOpenAI(api_key=api_key, model=model_name)` to use the new model class (e.g., `self.llm = ChatGoogleGenerativeAI(api_key=api_key, model=model_name)`). You may also need to adjust the `model` parameter to match the new provider's model naming conventions.
4.  **Update environment variables**: Ensure the correct API key environment variable is set for your chosen provider (e.g., `GOOGLE_API_KEY` for Google AI).

### Reverting to Groq

If you want to revert back to Groq:
1. Uncomment the Groq-related lines in `requirements.txt`, `llm_client.py`, and all command files
2. Comment out the OpenAI-related lines
3. Update your `.env` file to use `GROQ_API` instead of `OPENAI_API_KEY`

This approach makes it relatively easy to swap out LLM providers due to Langchain's consistent interface.

## Usage

### Convenience Scripts

For easier workflow, use the provided shell scripts in the `scripts/` directory that read configuration from your `.env` file:

```bash
# 1. Interactive repository selection and PR fetching
./scripts/1-pull-prs.sh

# 2. Rate the fetched PRs against KSBs
./scripts/2-rate-work.sh

# 3. Generate the final portfolio
./scripts/3-write-portfolio.sh
```

### Manual CLI Usage

Alternatively, all commands can be run directly via `python cli.py <command>`.

### 1. Pull Pull Requests

Fetches pull requests for a specified GitHub username.

```bash
python cli.py pull-prs --username <your_github_username>
```

*   `<your_github_username>`: The GitHub username to fetch PRs for (e.g., `patdel0`).

Example:
```bash
python cli.py pull-prs --username patdel0
```
This will save the fetched PRs to `output/pull_requests.csv`. This command is the first step in the portfolio generation process, providing the raw data for subsequent assessment.

### 2. Rate Work

Assesses the pulled PRs against the KSBs defined in `ksbs.csv` using the configured LLM.

```bash
python cli.py rate-work
```

This command will generate `rated_work.csv` containing the assessment results.

### 3. Write Portfolio

Generates the final portfolio markdown file (`output/portfolio.md`) based on the rated work. This command first identifies the highest-rated PRs for each KSB from `output/rated_work.csv` and then uses these to construct detailed narrative chapters.

```bash
python cli.py write-portfolio
```

This command will create `portfolio.md` in the project root, containing narrative chapters for each KSB.

### Post-Generation Steps

After generating `portfolio.md`, you will find placeholders for images and code snippets that need to be manually replaced with actual content. These placeholders are in the format:

*   `[==insert image of: a brief description of the visual==]`
*   `[==insert code snippet of: a brief description of the code==]`

To finalize your portfolio, locate these tags in `output/portfolio.md` and replace them with relevant images (e.g., screenshots, diagrams) or actual code blocks that provide concrete evidence of your work. The description within the tags will guide you on what content is needed.

To easily find all placeholders, you can use the following command:
```bash
grep -n "==insert" output/portfolio.md
```
This command will show you the line number and the content of each line containing a placeholder.

### Converting to Other Formats

For converting `portfolio.md` to various formats (e.g., PDF, HTML, DOCX), Pandoc is a highly recommended and versatile tool.

## Mitigating Repetitive Content

A known challenge with using LLMs for generative tasks is the potential for repetitive output, as the model has no memory of previously generated content. To combat this, the portfolio generator uses a "variety toolkit" approach.

Instead of a single, static prompt, it dynamically constructs a unique prompt for each portfolio chapter by randomly selecting from a predefined set of:

*   **Narrative Angles:** (e.g., framing the work as a detective story, a collaboration, or a refactoring effort).
*   **Opening Hooks:** To ensure varied introductory sentences.
*   **Reflection Phrases:** To avoid repeating the same conclusions.

This method forces stylistic diversity across chapters, resulting in a more natural and engaging portfolio.

## Project Structure

The project follows Python packaging best practices with a clean separation of concerns:

```
ksb-logger/
├── ksb_logger/                 # Main Python package
│   ├── __init__.py
│   ├── cli.py                  # CLI interface implementation
│   ├── clients/                # External service clients
│   │   ├── __init__.py
│   │   ├── github_client.py    # GitHub API integration
│   │   └── llm_client.py       # LLM integration (OpenAI)
│   ├── commands/               # CLI command implementations
│   │   ├── __init__.py
│   │   ├── extract_style.py    # Style analysis command
│   │   ├── pull_prs.py         # PR fetching command
│   │   ├── rate_work.py        # PR rating command
│   │   └── write_portfolio.py  # Portfolio generation command
│   ├── core/                   # Core business logic
│   │   ├── __init__.py
│   │   ├── data_persistence.py # CSV file handling
│   │   ├── ksb_loader.py       # KSB definitions loader
│   │   ├── portfolio_generator.py # Portfolio generation logic
│   │   └── repo_selector.py    # Interactive repository selection
│   └── data/                   # Static data files
│       ├── ksbs.csv            # KSB definitions
│       └── prompts/            # LLM prompt templates
├── scripts/                    # Convenience shell scripts
│   ├── 1-pull-prs.sh          # Interactive PR fetching
│   ├── 2-rate-work.sh         # Rate PRs against KSBs
│   └── 3-write-portfolio.sh   # Generate final portfolio
├── output/                     # Generated files (ignored by git)
│   ├── pull_requests.csv      # Fetched PR data
│   ├── rated_work.csv         # PR assessment results
│   └── portfolio.md           # Final portfolio
├── cli.py                      # Main entry point (wrapper)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (ignored by git)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

### Key Components

- **`cli.py`**: Main entry point that delegates to the package CLI
- **`ksb_logger/`**: Core package containing all business logic
- **`clients/`**: External service integrations (GitHub, OpenAI)
- **`commands/`**: Individual CLI command implementations
- **`core/`**: Core business logic and data handling
- **`data/`**: Static configuration and prompt files
- **`scripts/`**: User-friendly shell scripts for common workflows
