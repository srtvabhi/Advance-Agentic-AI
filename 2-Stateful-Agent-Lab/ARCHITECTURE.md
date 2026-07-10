# Stateful Agent Lab Architecture

## Objective

Build a stateful agent workflow design using the OpenAI Agents SDK.

This lab demonstrates how an agent can remember previous conversation messages during the same running session.

This type of memory is called:

- Short-term memory
- Session memory
- Conversation memory

## Architecture Flow

```text
User Message
   |
   v
main.py
   |
   v
Memory.py stores user message
   |
   v
Stateful Agent receives full conversation history
   |
   v
Agent responds using previous context
   |
   v
Memory.py updates conversation history
   |
   v
Next user message continues with memory
```

## Folder Structure

```text
2-Stateful-Agent-Lab/
├── .env
├── requirements.txt
├── main.py
├── Memory.py
├── config/
│   └── settings.py
├── agent/
│   └── stateful_agent.py
└── models/
    └── conversation_models.py
```

## File Responsibilities

### main.py

This is the entry point of the lab.

It performs these steps:

1. Loads Azure OpenAI configuration.
2. Creates the stateful agent.
3. Creates the conversation memory object.
4. Accepts user messages in a loop.
5. Stores each user message in memory.
6. Sends the full memory to the agent.
7. Prints the agent response.
8. Updates memory after every agent response.

### Memory.py

This file contains the `ConversationMemory` class.

It stores previous conversation messages in this list:

```python
self.input_items = []
```

This list is passed back to the agent on every turn.

Important methods:

```python
add_user_message()
get_items()
update_from_result()
clear()
show_memory()
```

### config/settings.py

This file handles Azure OpenAI configuration.

It reads values from the local `.env` file:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
```

It also creates the OpenAI client used by the OpenAI Agents SDK.

### agent/stateful_agent.py

This file creates the Stateful Workflow Agent.

The agent is instructed to:

- Use previous conversation messages
- Answer follow-up questions
- Remember useful session context
- Explain stateful workflow concepts simply

### models/conversation_models.py

This file defines the `MemoryItem` dataclass.

It is used to display stored memory in a readable format when the user types:

```text
memory
```

## What Kind Of Memory This Lab Maintains

This lab maintains in-memory session memory.

It can remember:

- User name
- Project name
- Previous questions
- Previous answers
- Decisions made in the current conversation
- Current workflow context
- Follow-up question context

Example:

```text
You: My name is Abhishek.
Agent: Nice to meet you, Abhishek.

You: What is my name?
Agent: Your name is Abhishek.
```

## Important Limitation

This memory is not permanent.

It is stored only while the Python program is running.

```text
Program running = memory available
Program closed = memory lost
```

This lab does not store memory in:

- File storage
- Database
- Redis
- Vector database
- Azure AI Search
- Cosmos DB

## Useful Commands Inside The App

### Show Memory

```text
memory
```

Displays the stored conversation messages.

### Clear Memory

```text
clear
```

Clears the current session memory.

### Exit

```text
exit
```

Stops the application.

## How To Run

From the root workspace folder:

```bash
cd 2-Stateful-Agent-Lab
..\.venv\Scripts\python.exe main.py
```

## Key Learning Points

This lab teaches:

- Stateless vs stateful agent behavior
- Short-term memory design
- Conversation history management
- Passing previous messages back to an agent
- How follow-up questions work
- How to clear or inspect memory

## Why This Architecture Is Useful

Stateful architecture is useful because real enterprise workflows often happen over multiple steps.

For example:

1. User gives project name.
2. User gives target audience.
3. User gives business goal.
4. Agent remembers all details.
5. Agent creates a final workflow using the full context.

Without memory, the user would need to repeat information again and again.

This lab shows the simplest version of that idea.
