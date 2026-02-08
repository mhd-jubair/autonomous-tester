# Autonomous Tester

An AI-powered autonomous software testing agent that can independently explore web applications and REST APIs, generate test cases, execute tests, detect defects, and generate comprehensive reports.

> **Note:** Currently, this project only supports **Azure OpenAI** for LLM and embedding services.

## Overview

Autonomous Tester uses a multi-agent AI system built with [CrewAI](https://github.com/crewAIInc/crewAI) to perform end-to-end testing of web applications and REST APIs. The system consists of three specialized agents:

1. **Test Planner** - Analyzes application requirements and creates test cases
2. **Test Specialist** - Executes tests using browser automation or API testing tools
3. **Report Specialist** - Compiles findings into a summary report

## Features

- Autonomous test case generation from requirements documents
- **Web UI Testing** - Browser-based test execution using [browser-use](https://github.com/browser-use/browser-use)
- **REST API Testing** - Comprehensive API testing with validation (status codes, JSON paths, headers, response time)
- Automated defect detection and reporting
- AI-powered test planning and analysis
- Sequential workflow: Planning → Execution → Reporting

## Requirements

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Azure OpenAI API access (for LLM and embeddings)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mhd-jubair/autonomous-tester.git
   cd autonomous-tester
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Configuration

Create a `.env` file in the project root with the following environment variables:

```env
# Azure OpenAI Configuration (Required)
AZURE_API_KEY=your_azure_api_key
AZURE_API_BASE=https://your-resource.openai.azure.com/
AZURE_API_VERSION=2024-10-21
MODEL=azure/your-deployment-name
EMBEDDING_MODEL=your-embedding-deployment-name

# Autonomous Tester Configuration (Optional)
AT_VERBOSE=true
AT_REQUIREMENTS_PATH=example/web_app/web_application.txt
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_API_KEY` | Your Azure OpenAI API key | Yes |
| `AZURE_API_BASE` | Azure OpenAI endpoint URL | Yes |
| `AZURE_API_VERSION` | Azure OpenAI API version | Yes |
| `MODEL` | LLM deployment name (e.g., `azure/gpt-4o`) | Yes |
| `EMBEDDING_MODEL` | Embedding model deployment name | Yes |
| `AT_VERBOSE` | Enable verbose logging (`true`/`false`) | No |
| `AT_REQUIREMENTS_PATH` | Path to requirements file | No |

## Usage

### Running the Autonomous Tester

```bash
uv run src/autonomous_tester/main.py --type <app_type> --endpoint <application_url>
```

#### Arguments

| Argument | Description | Required | Values |
|----------|-------------|----------|--------|
| `--type` | Type of application to test | Yes | `web_app`, `api_app` |
| `--endpoint` | URL of the application to test | Yes | Any valid URL |

#### Examples

```bash
# Test a web application
uv run src/autonomous_tester/main.py --type web_app --endpoint http://localhost:5000

# Test a REST API
uv run src/autonomous_tester/main.py --type api_app --endpoint http://localhost:8000
```

### Using Make Commands

The project includes convenient Make commands for running with example applications:

```bash
# Web Application Testing
make webapp-real        # Test the correct web app (no defects)
make webapp-defected    # Test the defected web app

# REST API Testing
make api-real           # Test the correct API (no defects)
make api-defected       # Test the defected API
```

## Project Structure

```
autonomous-tester/
├── src/
│   └── autonomous_tester/
│       ├── main.py                           # Entry point
│       ├── libs/
│       │   ├── common/
│       │   │   ├── config.py                 # Settings and configurations
│       │   │   ├── decorators.py             # Common decorators
│       │   │   ├── logger.py                 # Logger configuration
│       │   │   └── task_manager.py           # Task collection manager
│       │   └── crew_tools/
│       │       ├── api_test_tool.py          # REST API testing tool
│       │       ├── browser_tool.py           # Browser automation tool
│       │       └── requirements_tool.py      # Requirements parsing tool
│       ├── tester_crew/
│       │   ├── tester_crew.py                # CrewAI crew definition
│       │   └── config/
│       │       ├── agents.yaml               # Agent configurations
│       │       ├── tasks.yaml                # Task configurations
│       │       └── task_collections.yaml     # Task templates per app type
│       └── utils/
│           └── dot_dict.py                   # Helper module for dict to dot_dict
├── example/
│   ├── web_app/
│   │   ├── app_real.py                       # Example web app (correct)
│   │   ├── app_defect.py                     # Example web app (with defect)
│   │   ├── web_application.txt               # Web app requirements document
│   │   └── templates/
│   │       └── index.html                    # Web UI template
│   └── api/
│       ├── auth_api_real.py                  # Example API (correct)
│       ├── auth_api_defect.py                # Example API (with defect)
│       └── API_application.txt               # API requirements document
├── design/
│   ├── architecture.md                       # System architecture diagram
│   └── class_diagram.md                      # Class diagram
├── pyproject.toml
├── Makefile
└── README.md
```

## Example Applications

The project includes example applications for demonstration:

### Web Application (Simple Adder)

- **Correct version** (`app_real.py`): Properly adds two numbers
- **Defected version** (`app_defect.py`): Contains an intentional bug (multiplies second number by 2)

```bash
# Start the correct application on port 5000
uv run example/web_app/app_real.py

# Start the defected application on port 5001
uv run example/web_app/app_defect.py
```

### REST API (Authentication API)

- **Correct version** (`auth_api_real.py`): Properly handles authentication
- **Defected version** (`auth_api_defect.py`): Contains intentional bugs

```bash
# Start the correct API on port 8000
uv run uvicorn example.api.auth_api_real:app --reload

# Start the defected API on port 8000
uv run uvicorn example.api.auth_api_defect:app --reload
```

## How It Works

1. **Test Planning**: The Test Planner agent reads the requirements document using a RAG-based tool and generates test cases with IDs, descriptions, pre-steps, and execution steps.

2. **Test Execution**: The Test Specialist agent uses the appropriate tool based on application type:
   - **Web Apps**: Browser automation to interact with the UI
   - **APIs**: HTTP requests with response validation

3. **Report Generation**: The Report Specialist agent compiles all findings into a summary table showing test results and a defect summary.

## Agents & Tools

| Agent | Role | Tools |
|-------|------|-------|
| Test Planner | Creates test cases from requirements | Requirements Search Tool |
| Test Specialist | Executes tests | Browser Tool, API Test Tool |
| Report Specialist | Generates summary reports | None |

### API Test Tool Capabilities

- All HTTP methods (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- Authentication support (Bearer token, Basic auth, API key)
- Response validation:
  - Status code matching
  - JSON path validation
  - Header validation
  - Response time assertions
  - Content matching

## Limitations

- **Azure OpenAI Only**: Currently only supports Azure OpenAI for LLM and embedding services
- **Sequential Processing**: Tests are executed sequentially, not in parallel

## License

This project is open source. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
Copyright © 2026 Mohamed Jubair M. All rights reserved.
