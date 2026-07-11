# Enterprise Agent Lab Architecture

## Objective

Build an enterprise-style tool-calling agent using the OpenAI Agents SDK.

This lab demonstrates how an agent can use multiple tools to answer user questions and call external services.

The agent can:

- Get the current date and time
- Perform basic calculations
- Get live weather from OpenWeatherMap
- Search the web using Serper

## Architecture Flow

```text
User Question
   |
   v
main.py
   |
   v
Enterprise Agent
   |
   +--> Date Time Tool
   |
   +--> Calculator Tool
   |
   +--> Weather Tool
   |       |
   |       v
   |   Weather Service
   |       |
   |       v
   |   OpenWeatherMap API
   |
   +--> Web Search Tool
           |
           v
       Search Service
           |
           v
       Serper API
```

## Folder Structure

```text
1- OpenAI Agent SDK-Enterprise-Agent-Lab/
├── .env
├── requirements.txt
├── main.py
├── config/
│   └── settings.py
├── agent/
│   └── enterprise_agent.py
├── tools/
│   ├── calculator.py
│   ├── weather.py
│   ├── search.py
│   └── datetime_tool.py
├── services/
│   ├── weather_service.py
│   └── search_service.py
└── models/
    └── response_models.py
```

## File Responsibilities

### main.py

This is the entry point of the lab.

It performs these steps:

1. Loads Azure OpenAI configuration.
2. Creates the enterprise agent.
3. Starts a chat loop.
4. Sends user questions to the agent.
5. Prints the agent response.

### config/settings.py

This file handles configuration.

It reads values from the local `.env` file:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
```

It also stores external API keys used by tools:

- OpenWeatherMap key
- Serper key

Finally, it creates the OpenAI client used by the OpenAI Agents SDK.

### agent/enterprise_agent.py

This file creates the Enterprise Tool Agent.

The agent is connected to four tools:

- `get_current_time`
- `calculate`
- `get_weather`
- `web_search`

The agent decides which tool to call based on the user question.

### tools/datetime_tool.py

This file defines the date and time tool.

It returns the current local system date and time.

Example prompt:

```text
What is the current time?
```

### tools/calculator.py

This file defines the calculator tool.

It evaluates simple math expressions.

Example prompt:

```text
Calculate 25 * 18 + 40
```

### tools/weather.py

This file defines the weather tool.

The tool itself is intentionally small. It calls the weather service:

```python
fetch_current_weather(city)
```

Example prompt:

```text
What is the weather in Mumbai?
```

### tools/search.py

This file defines the web search tool.

The tool itself is intentionally small. It calls the search service:

```python
search_web(query)
```

Example prompt:

```text
Search the web for latest Azure AI Foundry updates
```

### services/weather_service.py

This file contains the OpenWeatherMap API logic.

It:

1. Builds the weather API URL.
2. Calls OpenWeatherMap.
3. Reads the JSON response.
4. Converts the response into a `WeatherResponse` model.
5. Returns a learner-friendly text response.

### services/search_service.py

This file contains the Serper API logic.

It:

1. Builds the web search request.
2. Calls Serper.
3. Reads the JSON response.
4. Converts top results into `SearchResult` models.
5. Returns a learner-friendly search summary.

### models/response_models.py

This file defines simple dataclasses for API responses.

It contains:

- `WeatherResponse`
- `SearchResult`

These models keep external API data organized before returning it to the agent.

## Why This Architecture Is Enterprise Style

This lab separates responsibilities:

- `main.py` runs the application.
- `agent/` defines agent behavior.
- `tools/` exposes actions to the agent.
- `services/` contains external API logic.
- `models/` organizes response data.
- `config/` handles environment and client setup.

This separation makes the application easier to:

- Understand
- Test
- Extend
- Debug
- Maintain

## Example Prompts

```text
What is the current time?
```

```text
Calculate 4500 / 15 + 280
```

```text
What is the weather in Delhi?
```

```text
Search the web for latest Azure AI Foundry updates
```

```text
I am building an enterprise HR helpdesk agent. Search the web for best practices and summarize them.
```

## How To Run

From the root workspace folder:

```bash
cd 1- OpenAI Agent SDK-Enterprise-Agent-Lab
..\.venv\Scripts\python.exe main.py
```

## Key Learning Points

This lab teaches:

- Tool-driven agent systems
- External API integration
- Enterprise folder structure
- Separation of tools and services
- Response modeling with dataclasses
- Using OpenAI Agents SDK with Azure AI Foundry

## How To Extend This Lab

You can add more tools by following this pattern:

1. Create a new service file in `services/`.
2. Create a new tool file in `tools/`.
3. Import the tool in `agent/enterprise_agent.py`.
4. Add the tool to the agent's `tools` list.
5. Update the agent instructions.

Example future tools:

- Create Jira ticket
- Send email
- Query HR policy
- Create ServiceNow incident
- Search internal knowledge base

