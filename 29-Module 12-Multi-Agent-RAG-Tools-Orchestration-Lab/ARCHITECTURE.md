# Multi-Agent RAG And Tools Orchestration Lab Architecture

## Objective

Implement multi-agent orchestration with RAG and tools using LangGraph.

This capstone lab combines retrieval, deterministic tools, planner-executor-reviewer agents, safety checks, and LangSmith tracing.

## Architecture Flow

```text
User Request
   |
   v
RAG Retrieval Node
   |
   v
Tool Execution Node
   |
   v
Planner Agent Node
   |
   v
Executor Agent Node
   |
   v
Reviewer Agent Node
   |
   v
Final Answer Node
```

## Folder Structure

```text
29-Module 12-Multi-Agent-RAG-Tools-Orchestration-Lab/
├── .env
├── .env.example
├── requirements.txt
├── main.py
├── ARCHITECTURE.md
├── config/
│   └── settings.py
├── data/
│   └── enterprise_policy_kb.txt
├── graphs/
│   └── orchestration_graph.py
├── nodes/
│   └── orchestration_nodes.py
├── services/
│   ├── llm_service.py
│   ├── retrieval_service.py
│   └── tool_service.py
└── models/
    └── orchestration_models.py
```

## Tree-Based Call Architecture

This view explains which file calls which function, starting from `main.py`.

```text
main.py
|
|-- imports: configure_langsmith()
|   from config/settings.py
|
|-- imports: build_orchestration_graph()
|   from graphs/orchestration_graph.py
|
|-- function: main()
    |
    |-- calls: configure_langsmith()
    |-- reads enterprise request
    |-- calls: build_orchestration_graph()
    |-- calls: app.invoke(initial OrchestrationState)
    |
    |-- LangGraph executes:
        |
        |-- rag_retrieval_node()
        |   |-- calls: retrieve_policy_context()
        |   |   from services/retrieval_service.py
        |   |-- writes retrieved_context
        |
        |-- tool_execution_node()
        |   |-- calls: run_enterprise_tools()
        |   |   from services/tool_service.py
        |   |-- writes tool_results
        |
        |-- planner_agent_node()
        |   |-- reads request, context, and tool results
        |   |-- calls: ask_model()
        |   |-- writes planner_output
        |
        |-- executor_agent_node()
        |   |-- reads planner_output
        |   |-- calls: ask_model()
        |   |-- writes executor_output
        |
        |-- reviewer_agent_node()
        |   |-- reads executor_output
        |   |-- calls: ask_model()
        |   |-- writes reviewer_output
        |
        |-- final_answer_node()
            |-- combines RAG, tools, planner, executor, and reviewer outputs
            |-- writes final_answer
```

## Tools Used

- `create_ticket`
- `check_approval_required`

## LangSmith Setup

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=module-12-multi-agent-rag-tools-lab
```

## How To Run

```bash
cd "29-Module 12-Multi-Agent-RAG-Tools-Orchestration-Lab"
..\.venv\Scripts\python.exe main.py
```

## Key Learning Points

- Multi-agent orchestration
- RAG grounding
- Tool-driven AI workflow
- Human approval detection
- Reviewer-validation pattern
- Traceable enterprise workflow execution
