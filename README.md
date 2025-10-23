# Zervem ETL API

A Flask-based ETL (Extract-Transform-Load) service that generates AI-powered competitive intelligence reports using Large Language Models (LLMs).

## Overview

The Zervem ETL API orchestrates sophisticated data pipelines that leverage OpenAI's GPT models to analyze companies, identify competitors, and generate comprehensive brand intelligence reports. The system features intelligent caching, dynamic module loading, and a clean layered architecture.

## Features

- **AI-Powered Analysis**: Integrates with OpenAI GPT models for competitor identification and market intelligence
- **Dynamic ETL Loading**: Automatically discovers and loads ETL report modules
- **Intelligent Caching**: Persists LLM responses to reduce API costs and enable rapid iteration
- **Brand Power Reports**: Comprehensive competitor analysis and brand positioning scoring
- **Conversation Context**: Maintains message history for contextual multi-turn LLM interactions
- **Extensible Architecture**: Factory pattern enables easy addition of new LLM providers
- **Machine Learning Toolkit**: Includes Jaccard, TF-IDF, and SBERT similarity algorithms

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────────┐
│     Controllers (HTTP Layer)            │
│  - ReportProcessorController            │
│  - AuthenticationController             │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Managers (Business Logic)           │
│  - ReportJobsTaskManager                │
│  - ReportProcessorResourceManager       │
│  - AIServiceHandler (Factory)           │
│  - OpenAIServiceManager                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     ETL Reports (Data Processing)       │
│  - BrandPower                           │
│  - CompetitorTracker                    │
└─────────────────────────────────────────┘
```

### Directory Structure

```
zervem-etl-api/
├── abstractions/              # Interfaces and base classes
│   ├── IController.py
│   ├── IETLServiceManager.py
│   ├── ILLMServiceManager.py
│   ├── EtlReportBase.py
│   ├── enumerations/
│   └── models/
├── controllers/               # HTTP endpoint handlers
│   ├── auth/
│   └── report_processor/
├── managers/                  # Business logic orchestration
│   ├── ReportJobsTaskManager.py
│   ├── ai/
│   ├── auth/
│   └── reports_processor/
├── models/                    # Request/response DTOs
│   ├── request/
│   └── response/
├── report_etls/              # ETL implementations
│   ├── brand_power.py
│   └── competitor_tracker.py
├── configs/                  # Configuration files
├── utility/                  # Helper classes
│   ├── Utility.py
│   └── MachineLearningToolkit.py
├── cache/                    # LLM response cache
├── logs/                     # Application logs
├── tests/                    # Unit tests
└── run_web_service.py       # Flask app entry point
```

## Prerequisites

- Python 3.6 or later
- pip (Python package installer)
- OpenAI API key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SwipeSwipeTeam/product-recsys-api.git
cd zervem-etl-api
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys and Credentials

**IMPORTANT: Never commit API keys or credentials to version control!**

The project uses configuration files in the `configs/` directory. Update these files with your credentials:

1. **ETL Configuration** (`configs/dev_etl_config.json`):
```json
{
  "web_api_config": {
    "base_url": "https://api.example.com",
    "credentials": {
      "username": "your-username",
      "password": "your-password"
    }
  }
}
```

2. **SERP API Configuration** (`configs/serp_config.json`):
```json
{
  "api_base_url": "https://serpapi.com/search.json",
  "api_filters": {
    "api_key": "your-serpapi-key-here",
    "engine": "google_shopping",
    "hl": "en",
    "gl": "us"
  },
  "query_keyword": "q",
  "result_config": {
    "related_shopping_items": "shopping_results",
    "nested_keys_to_use": {
      "product_title": "title",
      "product_id": "product_id",
      "url": "product_link",
      "merchant": "source",
      "price": "extracted_price",
      "position_rank": "position",
      "rating": "rating",
      "reviews": "reviews",
      "product_image": "thumbnail"
    }
  }
}
```

3. **ML Configuration** (`configs/ml_config.json`):
```json
{
  "default_model": "all-MiniLM-L6-v2"
}
```

4. **Web Configuration** (`configs/web_config.json`):
```json
{
  "dev": {
    "host": "",
    "https": true
  }
}
```

**Security Best Practices:**
- Add `configs/*.json` to `.gitignore` if they contain sensitive data
- Use environment variables for production deployments
- Create template config files (e.g., `config.json.example`) for documentation
- Rotate API keys regularly

## Usage

### Running the Service

**Development Mode:**
```bash
python3 run_web_service.py
```

The API will start on `http://0.0.0.0:5001`

**Docker:**
```bash
docker-compose build
docker-compose up
```

## API Endpoints

### Start ETL Report Job

**Endpoint:** `POST /report_processor/start_job`

**Request Body:**
```json
{
  "report_name": "brand_power",
  "task_params": {
    "target_industries": ["Technology", "AI"],
    "company_name": "Zerveme",
    "description_of_company": "AI-powered data platform",
    "company_website": "www.zerveme.com",
    "location": "USA",
    "known_competitors": ["Competitor1", "Competitor2"],
    "use_cache": true
  },
  "llm_config": {
    "ai_type": "openai",
    "api_key": "sk-...",
    "model_name": "gpt-4o",
    "gen_config": {
      "temperature": 0.7,
      "max_output_tokens": 2048
    }
  }
}
```

**Response:**
```json
{
  "message": "Post request on task",
  "data": []
}
```

### Brand Power Report Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `target_industries` | array | Yes | Industries to analyze (e.g., ["Technology", "AI"]) |
| `company_name` | string | Yes | Target company name |
| `description_of_company` | string | Yes | Company description |
| `company_website` | string | Yes | Company website URL |
| `location` | string | Yes | Company location |
| `known_competitors` | array | No | List of known competitors |
| `use_cache` | boolean | No | Use cached LLM responses (default: true) |

## Available Reports

### 1. Brand Power

**Report Name:** `brand_power`

**Description:** Analyzes a company's brand positioning versus competitors in specified industries.

**Process:**
1. **Pre-Validation**: Validates input parameters and industry validity
2. **Extract**:
   - Queries LLM to identify top 10 competitors
   - Retrieves competitor traits, descriptions, and sources
   - Gathers industry news source rankings
   - Caches all LLM responses
3. **Transform**: Calculates brand power scores (in progress)
4. **Post-Validation**: Validates output data

**Cache Location:** `cache/brand_power.json`

### 2. Competitor Tracker

**Report Name:** `competitor_tracker`

**Status:** Stub implementation (in development)

## LLM Configuration

### Supported LLM Providers

- **OpenAI** (Implemented)
  - GPT-4o
  - GPT-4 Turbo
  - GPT-3.5 Turbo
- **Google Generative AI** (Planned)

### LLM Configuration Options

**Note:** The OpenAI API key should be passed in the request body, not stored in config files.

```json
{
  "ai_type": "openai",
  "api_key": "sk-your-openai-api-key-here",
  "model_name": "gpt-4o",
  "gen_config": {
    "temperature": 0.7,
    "max_output_tokens": 2048
  }
}
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ai_type` | LLM provider ("openai", "google_generative_ai") | Required |
| `api_key` | API key for the LLM provider | Required |
| `model_name` | Specific model to use | Required |
| `temperature` | Randomness in responses (0-2) | 0.7 |
| `max_output_tokens` | Maximum response length | 2048 |

## Caching System

The API implements intelligent caching to reduce LLM API costs:

- **Automatic Caching**: All LLM responses are automatically cached
- **Cache Location**: `cache/{report_name}.json`
- **Cache Control**: Set `use_cache: true` in task_params to use cached responses
- **Manual Cache Clearing**: Delete cache files to force fresh LLM calls

### Cache Structure

```json
{
  "target_company": {
    "name": "Company Name",
    "competitors": [...],
    "sources_from_pull": [...]
  },
  "competitor_data": [...]
}
```

## Machine Learning Toolkit

The utility module includes three similarity algorithms:

### 1. Jaccard Similarity
- Fast, simple string matching
- Best for exact matches
- Range: 0-1 (1 = identical)

### 2. TF-IDF + Cosine Similarity
- Term frequency-based vectorization
- Better for semantic similarity
- Medium computational cost

### 3. Sentence-BERT (SBERT)
- Pre-trained language model embeddings
- Best for understanding meaning
- Highest computational cost

## Development

### Branching Rules

**Feature Branches:**
```bash
git checkout -b feature/<jira#>-<description>
# Example: feature/ZM-149-AI-Service-Manager
```

**Bugfix Branches:**
```bash
git checkout -b bugfix/<jira#>-<description>
# Example: bugfix/1234-fix-caching
```

**Note:** Always create a pull request before merging into `develop`.

### Running Tests

```bash
python -m pytest tests/
```

### Code Quality

The project uses Flake8 for code linting:

```bash
flake8 .
```

## Creating New ETL Reports

To create a new ETL report:

1. Create a new file in `report_etls/` (e.g., `my_report.py`)
2. Inherit from `EtlReportBase`
3. Implement required methods:
   - `configure_init_tasks()`
   - `run_pre_validation()`
   - `run_extract_tasks()`
   - `run_transform_process_tasks()`
   - `run_post_validation()`

**Example:**

```python
from abstractions.EtlReportBase import EtlReportBase

class MyReport(EtlReportBase):
    def __init__(self, run_params: dict, llm_service_manager):
        super().__init__(run_params, llm_service_manager, "my_report")

    def configure_init_tasks(self):
        self.tasks_pipeline = {
            "pre_validation": [self.run_pre_validation],
            "extract": [self.run_extract_tasks],
            "transform": [self.run_transform_process_tasks],
            "post_validation": [self.run_post_validation],
        }

    def run_pre_validation(self):
        # Validate input parameters
        pass

    def run_extract_tasks(self):
        # Extract data from LLM or external sources
        pass

    def run_transform_process_tasks(self):
        # Transform and process data
        pass

    def run_post_validation(self):
        # Validate output
        pass
```

The report will be automatically discovered and loaded by `ReportJobsTaskManager`.

## Adding New LLM Providers

To add a new LLM provider:

1. Create a new manager in `managers/ai/` (e.g., `ClaudeServiceManager.py`)
2. Inherit from `ILLMServiceManager`
3. Implement `configure()` and `run_task()` methods
4. Update `AIServiceHandler.get_ai_service()` to include new provider
5. Add to `AiTypeEnum`

**Example:**

```python
from abstractions.ILLMServiceManager import ILLMServiceManager

class ClaudeServiceManager(ILLMServiceManager):
    def configure(self, **kwargs):
        # Initialize Claude client
        pass

    def run_task(self, request: LLMRequestResourceModel):
        # Call Claude API and return LLMResponseResourceModel
        pass
```

## Configuration Files

- `configs/dev_etl_config.json`: ETL service configuration
- `configs/ml_config.json`: Machine learning model settings
- `configs/serp_config.json`: Search engine API configuration
- `configs/web_config.json`: Web service settings

## Technology Stack

| Category | Technology | Version |
|----------|-----------|---------|
| Web Framework | Flask | 3.0.3 |
| Web Server | Gunicorn | 23.0.0 |
| CORS | Flask-CORS | 5.0.0 |
| LLM Integration | OpenAI Python SDK | ≥1.97.1 |
| AI Embeddings | Sentence-Transformers | 3.3.0 |
| ML/Statistics | Scikit-learn | 1.5.2 |
| Data Processing | Pandas | 2.2.3 |
| Numerical | NumPy | 2.1.3 |
| Code Quality | Flake8 | ≥6.1.0 |

## Design Patterns

- **Factory Pattern**: Dynamic LLM service instantiation
- **Strategy Pattern**: Pluggable LLM provider implementations
- **Template Method Pattern**: ETL workflow defined in `EtlReportBase`
- **Pipeline Pattern**: Sequential task execution
- **Dependency Injection**: Constructor-based injection
- **Interface Segregation**: Separate interfaces for different concerns

## Logging

Logs are written to:
- Console (stdout)
- `logs/{date}.log`

Log format:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Configuration Management

### Configuration Files

The application uses JSON configuration files in the `configs/` directory:

| File | Purpose | Contains Secrets |
|------|---------|------------------|
| `dev_etl_config.json` | ETL service configuration with API credentials | ⚠️ Yes |
| `serp_config.json` | SerpAPI configuration and key | ⚠️ Yes |
| `ml_config.json` | ML model settings | No |
| `web_config.json` | Web service settings | No |

### Security Considerations

**Current Configuration Structure:**
- API keys and credentials are stored in JSON files
- Ensure these files are properly secured and not committed to public repositories
- Check `.gitignore` includes sensitive config files

**Recommended for Production:**
- Use environment variables for sensitive data
- Implement a secrets management system (e.g., AWS Secrets Manager, HashiCorp Vault)
- Use different config files per environment (dev, staging, production)

## Troubleshooting

### Common Issues

**Issue:** `ImportError: No module named 'flask'`
- **Solution:** Ensure virtual environment is activated and dependencies are installed

**Issue:** LLM API rate limit errors
- **Solution:** Enable caching with `use_cache: true` to reuse previous responses

**Issue:** Cache not working
- **Solution:** Check that `cache/` directory exists and has write permissions

**Issue:** Report not found
- **Solution:** Ensure report file name matches the `report_name` in the request

## Contributing

1. Create a feature/bugfix branch following the naming convention
2. Make your changes with appropriate tests
3. Run `flake8` to ensure code quality
4. Create a pull request to `develop` branch

## License

[License information to be added]

## Contact

For questions or issues, please contact the development team or create an issue in the repository.

## Roadmap

### In Progress
- [ ] Complete `__transform_and_generate_report()` implementation
- [ ] Brand power scoring algorithm
- [ ] Report generation and formatting

### Planned Features
- [ ] Job status tracking and persistence
- [ ] Stop job functionality
- [ ] Google Generative AI integration
- [ ] Anthropic Claude integration
- [ ] Authentication/authorization (JWT)
- [ ] Database storage for results
- [ ] Async task execution
- [ ] Rate limiting and batch processing
- [ ] Enhanced monitoring and observability
- [ ] Web dashboard for report visualization

## Acknowledgments

Built with Flask, OpenAI, and open-source ML libraries.
