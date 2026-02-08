# Autonomous Tester

An AI-powered autonomous software testing agent that can independently explore web applications, generate test cases, execute tests, detect defects, and generate comprehensive reports.

> **Note:** Currently, this project only supports **Azure OpenAI** for LLM and embedding services.

## Overview

Autonomous Tester uses a multi-agent AI system built with [CrewAI](https://github.com/crewAIInc/crewAI) to perform end-to-end testing of web applications. The system consists of three specialized agents:

1. **Test Planner** - Analyzes application requirements and creates test cases
2. **Test Specialist** - Executes tests using browser automation
3. **Report Specialist** - Compiles findings into a summary report

## Features

- Autonomous test case generation from requirements documents
- Browser-based test execution using [browser-use](https://github.com/browser-use/browser-use)
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
AT_REQUIREMENTS_PATH=example/web_app/application.txt
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
uv run autonomous-tester --endpoint <web_application_url>
```

Example:
```bash
uv run autonomous-tester --endpoint http://localhost:5000
```

### Using Make Commands

The project includes convenient Make commands for running with example applications:

```bash
# Run tester against the correct (no defects) example application
make run-real

# Run tester against the defected example application
make run-defected
```

## Project Structure

```
autonomous-tester/
├── src/
│   └── autonomous_tester/
│       ├── main.py                           # Entry point
│       ├── libs/
│       │   ├── common/
|       |   |   ├── config.py                 # Settings and configurations
|       |   |   ├── decorators.py             # Common decorators
│       │   │   └── logger.py                 # Logger configuration
│       │   └── crew_tools/
│       │       ├── browser_tool.py           # Browser automation tool
│       │       └── requirements_tool.py      # Requirements parsing tool
│       ├── tester_crew/
│       |   ├── tester_crew.py                # CrewAI crew definition
│       |   └── config/
│       |       ├── agents.yaml               # Agent configurations
│       |       └── tasks.yaml                # Task configurations
|       └── utils/
|           └── dot_dict.py                   # Helper module for dict to dot_dict   
|       
├── example/
│   └── web_app/
│       ├── app_real.py                       # Example app (correct)
│       ├── app_defect.py                     # Example app (with defect)
│       ├── application.txt                   # Requirements document
│       └── templates/
│           └── index.html                    # Web UI template
├── pyproject.toml
├── Makefile
└── README.md
```

## Example Application

The project includes an example web application (Simple Adder) for demonstration:

- **Correct version** (`app_real.py`): Properly adds two numbers
- **Defected version** (`app_defect.py`): Contains an intentional bug (multiplies second number by 2)

### Running Example Applications

```bash
# Start the correct application on port 5000
uv run example/web_app/app_real.py

# Start the defected application on port 5001
uv run example/web_app/app_defect.py
```

## How It Works

1. **Test Planning**: The Test Planner agent reads the requirements document using a RAG-based tool and generates test cases with IDs, descriptions, pre-steps, and execution steps.

2. **Test Execution**: The Test Specialist agent uses browser automation to execute each test case against the target web application, recording pass/fail status and any defects found.

3. **Report Generation**: The Report Specialist agent compiles all findings into a summary table showing test results and a defect summary.

## Agents

| Agent | Role | Tools |
|-------|------|-------|
| Test Planner | Creates test cases from requirements | Requirements Search Tool |
| Test Specialist | Executes tests via browser | Browser Tool |
| Report Specialist | Generates summary reports | None |

## Limitations

- **Azure OpenAI Only**: Currently only supports Azure OpenAI for LLM and embedding services
- **Web Applications**: Designed specifically for testing web-based applications
- **Sequential Processing**: Tests are executed sequentially, not in parallel

## License

This project is open source. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
