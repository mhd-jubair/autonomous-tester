# Autonomous Tester - Class Diagram

```mermaid
classDiagram
    direction TB

    %% ============================================
    %% External Dependencies (CrewAI Framework)
    %% ============================================
    class CrewBase {
        <<decorator>>
    }
    
    class BaseTool {
        <<abstract>>
        +name: str
        +description: str
        +_run(query: str) str
    }
    
    class BaseAgent {
        <<abstract>>
    }
    
    class Agent {
        +config: dict
        +verbose: bool
        +tools: List
    }
    
    class Task {
        +config: dict
        +context: List~Task~
        +output_file: str
        +markdown: bool
    }
    
    class Crew {
        +agents: List~Agent~
        +tasks: List~Task~
        +process: Process
        +verbose: bool
        +kickoff(inputs: dict) void
    }
    
    class Process {
        <<enumeration>>
        sequential
        hierarchical
    }

    class TXTSearchTool {
        +txt: str
        +config: dict
    }

    class BaseModel {
        <<pydantic>>
        +model_dump() dict
    }

    %% ============================================
    %% Configuration Module
    %% ============================================
    class BASE {
        <<static>>
        +BASE_DIR: str
        +CONFIG_BASE: str
        +WEBAPP_REQUIREMENTS_PATH: str
        +API_REQUIREMENTS_PATH: str
    }
    
    class Settings {
        +VERBOSE: bool
        +REQUIREMENTS_PATH: str
        +AGENTS_CONFIG: str
        +TASKS_CONFIG: str
        +TASK_COLLECTIONS: str
        +STORAGE_DIR: str
        +__init__() void
    }

    %% ============================================
    %% Core Tester Crew Module
    %% ============================================
    class AutonomousTester {
        <<CrewBase>>
        +agents: List~BaseAgent~
        +tasks: List~Task~
        +settings: Settings
        +agents_config: str
        +tasks_config: str
        +test_planner() Agent
        +test_specialist() Agent
        +report_specialist() Agent
        +test_planning() Task
        +test_execution() Task
        +report_generation() Task
        +crew() Crew
    }

    %% ============================================
    %% Tools Module
    %% ============================================
    class BrowserTool {
        +name: str
        +description: str
        -_browser: Browser
        -_get_llm() ChatAzureOpenAI
        -_get_browser() Browser
        -_async_run(query: str) str
        +_run(query: str) str
        +__del__() void
    }
    
    class APITestTool {
        +name: str
        +description: str
        -_parse_input(query: str) Dict
        -_prepare_auth(auth_config: Dict) Any
        -_get_json_path_value(data: Any, path: str) Any
        -_validate_response(response: Response, validations: Dict) List
        +_run(query: str) str
    }
    
    class HttpMethod {
        <<enumeration>>
        GET
        POST
        PUT
        PATCH
        DELETE
        HEAD
        OPTIONS
    }
    
    class APITestResult {
        +success: bool
        +status_code: int
        +response_time_ms: float
        +response_body: Union~Dict, List, str~
        +headers: Dict~str, str~
        +error: str
        +validations: List~str~
    }

    %% ============================================
    %% Utilities Module
    %% ============================================
    class DotDict {
        +__init__(*args, **kwargs) void
        +__getattr__(item) Any
        +__setattr__(key, value) void
    }

    %% ============================================
    %% Task Manager Module
    %% ============================================
    class TaskManager {
        <<module>>
        +_load_task_collections() dict
        +manage_tasks(type: str, **kwargs) str
    }

    %% ============================================
    %% Main Entry Point
    %% ============================================
    class Main {
        <<module>>
        +main(type: str, **kwargs) void
    }

    %% ============================================
    %% Singleton Factory
    %% ============================================
    class singleton {
        <<decorator>>
        -result: Any
        -executed: bool
        +wrapper(*args, **kwargs) Any
    }

    %% ============================================
    %% Tool Factory
    %% ============================================
    class tester_tools {
        <<DotDict>>
        +requirements_tool: Function
        +browser_tool: BrowserTool
        +api_tool: APITestTool
    }

    %% ============================================
    %% Relationships
    %% ============================================
    
    %% Inheritance
    BrowserTool --|> BaseTool : extends
    APITestTool --|> BaseTool : extends
    TXTSearchTool --|> BaseTool : extends
    DotDict --|> dict : extends
    APITestResult --|> BaseModel : extends
    Agent --|> BaseAgent : extends

    %% Composition
    AutonomousTester *-- Settings : uses
    AutonomousTester *-- Agent : creates
    AutonomousTester *-- Task : creates
    AutonomousTester *-- Crew : creates
    Crew *-- Agent : contains
    Crew *-- Task : contains
    Crew o-- Process : uses

    %% Dependencies
    Main ..> AutonomousTester : instantiates
    Main ..> TaskManager : calls manage_tasks
    AutonomousTester ..> tester_tools : uses tools
    tester_tools ..> BrowserTool : contains
    tester_tools ..> APITestTool : contains
    tester_tools ..> TXTSearchTool : creates via get_requirements

    %% Factory patterns
    singleton ..> Settings : creates
    APITestTool ..> APITestResult : produces
    APITestTool ..> HttpMethod : uses

    %% Configuration
    Settings ..> BASE : reads defaults
    CrewBase ..> AutonomousTester : decorates

    %% Tool assignment to agents
    Agent o-- BaseTool : uses

```

## Class Descriptions

### Core Components

| Class | Description |
|-------|-------------|
| `AutonomousTester` | Main crew orchestrator decorated with `@CrewBase`. Creates and manages agents, tasks, and the crew workflow. |
| `Settings` | Configuration class that loads environment variables and provides paths for config files. |
| `BASE` | Static configuration holding base directory paths and default requirements file locations. |

### Agents & Tasks

| Component | Role |
|-----------|------|
| `test_planner` | Agent responsible for planning the testing strategy using requirements tool. |
| `test_specialist` | Agent that executes tests using browser and API tools. |
| `report_specialist` | Agent that generates test reports from execution results. |
| `test_planning` | Task for creating the test strategy. |
| `test_execution` | Task for running tests (depends on test_planning). |
| `report_generation` | Task for generating markdown reports (depends on test_execution). |

### Tools

| Tool | Purpose |
|------|---------|
| `BrowserTool` | Performs browser automation tasks using `browser_use` library. Supports async operations. |
| `APITestTool` | Tests REST APIs with validation capabilities (status codes, headers, JSON paths, response time). |
| `TXTSearchTool` | Searches requirements documents using embeddings (from crewai_tools). |

### Utilities

| Utility | Purpose |
|---------|---------|
| `DotDict` | Dictionary subclass enabling dot-notation access (`d.key` instead of `d['key']`). |
| `APITestResult` | Pydantic model for structured API test results. |
| `HttpMethod` | Enum defining supported HTTP methods. |
| `singleton` | Decorator ensuring single instance creation for functions like `get_settings()`. |

### Data Flow

```
main() 
  → manage_tasks() → loads task_collections.yaml
  → AutonomousTester().crew() 
    → creates agents with tools
    → creates tasks with dependencies
    → Crew.kickoff(inputs) → sequential execution
```
