# Autonomous Tester - Architecture

## Overview

The **Autonomous Tester** is an AI-powered testing framework built on [CrewAI](https://www.crewai.com/) that automates software testing through intelligent agents. It leverages Large Language Models (LLMs) to understand application requirements, generate test strategies, execute tests, and produce comprehensive reports.

### Key Capabilities

- **Automated Test Planning** — Analyzes requirements documents to create testing strategies
- **Multi-Protocol Testing** — Supports both Web UI (browser automation) and REST API testing
- **Intelligent Validation** — Validates responses against expected outcomes using AI reasoning
- **Automated Reporting** — Generates detailed markdown reports with bug detections

---

## High-Level Architecture

```mermaid
graph TB
    subgraph INPUT["📥 Input Layer"]
        Req["📄 Application<br/>Requirements"]
        Config["⚙️ Configuration<br/>(YAML)"]
    end

    subgraph STORAGE["💾 Knowledge Store"]
        VectorDB[("🗄️ Vector Database<br/>(ChromaDB)")]
        Embeddings["🔢 Azure OpenAI<br/>Embeddings"]
    end

    subgraph ORCHESTRATION["🎯 Orchestration Layer"]
        direction TB
        Crew["🚀 CrewAI<br/>Orchestrator"]
        
        subgraph AGENTS["🤖 AI Agents"]
            Planner["📋 Test Planner<br/>Agent"]
            Specialist["🔬 Test Specialist<br/>Agent"]
            Reporter["📊 Report Specialist<br/>Agent"]
        end
    end

    subgraph LLM_LAYER["🧠 Intelligence Layer"]
        LLM["☁️ Azure OpenAI<br/>LLM"]
    end

    subgraph TOOLS["🛠️ Tools Layer"]
        ReqTool["📖 Requirements<br/>Search Tool"]
        BrowserTool["🌐 Browser<br/>Automation Tool"]
        APITool["🔌 API Test<br/>Tool"]
    end

    subgraph TARGET["🎯 Target Systems"]
        WebApp["🖥️ Web<br/>Application"]
        APIApp["📡 REST<br/>API"]
    end

    subgraph OUTPUT["📤 Output Layer"]
        Report["📝 Test Report<br/>(Markdown)"]
        Bugs["🐛 Bug<br/>Detections"]
    end

    %% Input Flow
    Req --> VectorDB
    Config --> Crew
    
    %% Knowledge Processing
    Embeddings --> VectorDB
    VectorDB --> ReqTool
    
    %% Agent Orchestration
    Crew --> Planner
    Planner --> Specialist
    Specialist --> Reporter
    
    %% LLM Connections
    LLM -.->|reasoning| Planner
    LLM -.->|reasoning| Specialist
    LLM -.->|reasoning| Reporter
    
    %% Tool Usage
    Planner -.->|query| ReqTool
    Specialist -.->|automate| BrowserTool
    Specialist -.->|test| APITool
    
    %% Target Interaction
    BrowserTool <-->|interact| WebApp
    APITool <-->|request/response| APIApp
    
    %% Output Generation
    Reporter --> Report
    Reporter --> Bugs

    %% Styling
    classDef inputStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef storageStyle fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef orchestrationStyle fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#e65100
    classDef agentStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#880e4f
    classDef llmStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c
    classDef toolStyle fill:#e0f7fa,stroke:#00838f,stroke-width:2px,color:#006064
    classDef targetStyle fill:#fff8e1,stroke:#f9a825,stroke-width:2px,color:#f57f17
    classDef outputStyle fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#b71c1c

    class Req,Config inputStyle
    class VectorDB,Embeddings storageStyle
    class Crew orchestrationStyle
    class Planner,Specialist,Reporter agentStyle
    class LLM llmStyle
    class ReqTool,BrowserTool,APITool toolStyle
    class WebApp,APIApp targetStyle
    class Report,Bugs outputStyle
```

---

## Component Details

### 📥 Input Layer

| Component | Description |
|-----------|-------------|
| **Application Requirements** | Text files describing the application's expected behavior and features |
| **Configuration (YAML)** | Agent definitions, task configurations, and task collections |

### 💾 Knowledge Store

| Component | Description |
|-----------|-------------|
| **Vector Database** | ChromaDB instance storing embedded requirements for semantic search |
| **Embeddings** | Azure OpenAI embedding model for converting text to vectors |

### 🎯 Orchestration Layer

| Component | Description |
|-----------|-------------|
| **CrewAI Orchestrator** | Manages sequential execution of agents and task dependencies |
| **Test Planner Agent** | Analyzes requirements and creates comprehensive test strategies |
| **Test Specialist Agent** | Executes test cases using browser and API tools |
| **Report Specialist Agent** | Synthesizes results into actionable bug reports |

### 🛠️ Tools Layer

| Tool | Purpose |
|------|---------|
| **Requirements Search Tool** | RAG-based semantic search over requirements documents |
| **Browser Automation Tool** | Headless browser control via `browser_use` library |
| **API Test Tool** | HTTP client with validation (status codes, JSON paths, headers) |

### 📤 Output Layer

| Output | Format |
|--------|--------|
| **Test Report** | Markdown file with detailed test results |
| **Bug Detections** | Structured findings with reproduction steps |

---

## Data Flow

```
1. Requirements (TXT) → Embedded → Vector DB
2. User triggers test with --type and --endpoint
3. CrewAI loads task description from task_collections.yaml
4. Sequential agent execution:
   ├─ Test Planner → reads requirements → outputs test plan
   ├─ Test Specialist → executes tests → outputs results  
   └─ Report Specialist → analyzes results → outputs report
5. Final report written to test_report.md
```

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Framework** | CrewAI |
| **LLM Provider** | Azure OpenAI |
| **Vector Store** | ChromaDB |
| **Browser Automation** | browser_use |
| **HTTP Client** | requests |
| **Configuration** | YAML, python-dotenv |
