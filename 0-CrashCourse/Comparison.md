# Agentic Framework Comparison

This file compares the frameworks used in the crash course and full labs.

## High-Level Comparison

| # | Framework | Best For | Main Style | Crash Course Folder |
|---|---|---|---|---|
| 1 | OpenAI Agents SDK | Simple agent apps, tool calling, handoffs, multi-agent workflows | Agent + Runner | `1-OpenAI-Agents-SDK` |
| 2 | LangGraph | Stateful graph workflows, routing, retries, multi-step orchestration | Graph nodes + edges | `2-LangGraph` |
| 3 | AutoGen | Multi-agent conversations and collaboration | Assistant agents + group chat | `3-AutoGen` |
| 4 | OpenAI SDK | Direct model calls and custom orchestration | API client + messages | `4-OpenAI-SDK` |
| 5 | ChromaDB RAG | Vector search and retrieval pipelines | Embeddings + vector store | `5-ChromaDB-RAG` |
| 6 | Semantic Kernel | Plugins, semantic functions, enterprise workflow orchestration | Kernel + plugins | `6-Semantic-Kernel` |

## Agent Creation Syntax

| Framework | Syntax | Example |
|---|---|---|
| OpenAI Agents SDK | `Agent(name=..., model=..., instructions=...)` | ```python\nagent = Agent(\n    name=\"Basic Assistant\",\n    model=os.environ[\"AZURE_OPENAI_DEPLOYMENT\"],\n    instructions=\"You are a helpful assistant.\",\n)\n``` |
| LangGraph | Create a node function and add it to `StateGraph` | ```python\ndef assistant_node(state):\n    state[\"answer\"] = ask_model(state[\"question\"])\n    return state\n\ngraph = StateGraph(AgentState)\ngraph.add_node(\"assistant\", assistant_node)\n``` |
| AutoGen | `AssistantAgent(name=..., model_client=..., system_message=...)` | ```python\nagent = AssistantAgent(\n    name=\"basic_autogen_agent\",\n    model_client=model_client,\n    system_message=\"You are a helpful assistant.\",\n)\n``` |
| OpenAI SDK | Use `client.chat.completions.create(...)` with system/user messages | ```python\nresponse = client.chat.completions.create(\n    model=os.environ[\"AZURE_OPENAI_DEPLOYMENT\"],\n    messages=[\n        {\"role\": \"system\", \"content\": \"You are a helpful assistant.\"},\n        {\"role\": \"user\", \"content\": question},\n    ],\n)\n``` |
| ChromaDB RAG | Agent is custom code: retrieve context, then call OpenAI SDK | ```python\ncontext = retrieve_policy(client, question)\nresponse = client.chat.completions.create(\n    model=os.environ[\"AZURE_OPENAI_DEPLOYMENT\"],\n    messages=[\n        {\"role\": \"system\", \"content\": \"Answer from context only.\"},\n        {\"role\": \"user\", \"content\": f\"Question: {question}\\nContext: {context}\"},\n    ],\n)\n``` |
| Semantic Kernel | Create `Kernel`, add chat service, then invoke prompt | ```python\nkernel = Kernel()\nkernel.add_service(OpenAIChatCompletion(\n    ai_model_id=os.environ[\"AZURE_OPENAI_DEPLOYMENT\"],\n    async_client=client,\n    service_id=\"foundry-chat\",\n))\n``` |

## Tool Calling Syntax

| Framework | Syntax | Example |
|---|---|---|
| OpenAI Agents SDK | Decorate a Python function with `@function_tool` | ```python\n@function_tool\ndef calculator(expression: str) -> str:\n    \"\"\"Calculate a simple math expression.\"\"\"\n    return calculate_expression(expression)\n``` |
| LangGraph | Put tool execution inside a graph node | ```python\ndef tool_node(state):\n    if \"calculate\" in state[\"question\"].lower():\n        state[\"tool_result\"] = calculator(\"40 * 5\")\n    return state\n``` |
| AutoGen | Pass Python functions in `tools=[...]` | ```python\nagent = AssistantAgent(\n    name=\"tool_autogen_agent\",\n    model_client=model_client,\n    tools=[calculator, get_weather],\n    max_tool_iterations=3,\n)\n``` |
| OpenAI SDK | Manually call tool function, then pass result to model | ```python\ntool_result = calculator(\"99 / 3\")\nresponse = client.chat.completions.create(\n    model=model_name,\n    messages=[\n        {\"role\": \"system\", \"content\": \"Answer using tool result.\"},\n        {\"role\": \"user\", \"content\": f\"Tool result: {tool_result}\"},\n    ],\n)\n``` |
| ChromaDB RAG | Retrieval is the tool: embed query, search vector DB | ```python\nresults = collection.query(\n    query_embeddings=[embed(client, question)],\n    n_results=2,\n)\ncontext = \"\\n\".join(results[\"documents\"][0])\n``` |
| Semantic Kernel | Use `@kernel_function` inside a plugin class | ```python\nclass UtilityPlugin:\n    @kernel_function(name=\"calculator\", description=\"Calculate math.\")\n    def calculator(self, expression: str) -> str:\n        return str(eval(expression, {\"__builtins__\": {}}, {}))\n\nkernel.add_plugin(UtilityPlugin(), plugin_name=\"Utility\")\n``` |

## Orchestration Syntax

| Framework | Syntax | Example |
|---|---|---|
| OpenAI Agents SDK | Run agents sequentially with `Runner.run` | ```python\nplan = await Runner.run(planner_agent, task)\nexecution = await Runner.run(executor_agent, plan.final_output)\nreview = await Runner.run(reviewer_agent, execution.final_output)\n``` |
| LangGraph | Connect nodes with edges | ```python\ngraph.add_node(\"planner\", planner_node)\ngraph.add_node(\"executor\", executor_node)\ngraph.add_node(\"reviewer\", reviewer_node)\ngraph.add_edge(\"planner\", \"executor\")\ngraph.add_edge(\"executor\", \"reviewer\")\ngraph.add_edge(\"reviewer\", END)\napp = graph.compile()\n``` |
| AutoGen | Use `RoundRobinGroupChat` | ```python\nteam = RoundRobinGroupChat(\n    [planner, executor, reviewer],\n    termination_condition=MaxMessageTermination(4),\n)\nresult = await team.run(task=\"Design a workflow\")\n``` |
| OpenAI SDK | Custom orchestration using multiple model calls | ```python\nplan = call_agent(client, \"planner instructions\", task)\nexecution = call_agent(client, \"executor instructions\", plan)\nreview = call_agent(client, \"reviewer instructions\", execution)\n``` |
| ChromaDB RAG | Coordinate retriever, answerer, reviewer functions | ```python\ncontext = retriever_agent(client, question)\nanswer = answer_agent(client, question, context)\nreview = reviewer_agent(client, answer)\n``` |
| Semantic Kernel | Coordinate semantic prompt functions or plugin calls | ```python\nplan = await planner_agent(kernel, task)\nexecution = await executor_agent(kernel, plan)\nreview = await reviewer_agent(kernel, execution)\n``` |

## When To Choose Which Framework

| Use Case | Recommended Framework |
|---|---|
| Beginner-friendly single agent with tools | OpenAI Agents SDK |
| Graph workflow with state, branching, retries | LangGraph |
| Multiple agents collaborating in conversation | AutoGen |
| Maximum control with minimal abstraction | OpenAI SDK |
| Retrieval and vector search | ChromaDB RAG |
| Enterprise plugin architecture and workflow automation | Semantic Kernel |

## Short Summary

| Framework | One-Line Summary |
|---|---|
| OpenAI Agents SDK | Fastest way to build agent apps with tools and orchestration. |
| LangGraph | Best when the workflow is a graph with state and routing. |
| AutoGen | Best for conversational multi-agent collaboration. |
| OpenAI SDK | Best for direct API control and custom patterns. |
| ChromaDB RAG | Best for local vector search and retrieval examples. |
| Semantic Kernel | Best for plugin-style enterprise AI orchestration. |
