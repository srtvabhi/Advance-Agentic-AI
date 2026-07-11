import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import asyncio
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import load_dotenv
from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments, kernel_function


OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"


class UtilityPlugin:
    # Tool: calculate simple arithmetic expressions safely.
    @kernel_function(name="calculator", description="Calculate a simple math expression.")
    def calculator(self, expression: str) -> str:
        allowed_chars = set("0123456789+-*/(). ")
        if not set(expression).issubset(allowed_chars):
            return "Invalid expression."
        try:
            return str(eval(expression, {"__builtins__": {}}, {}))
        except Exception as exc:
            return f"Calculation error: {exc}"

    # Tool: call OpenWeatherMap and return current weather for a city.
    @kernel_function(name="get_weather", description="Get current weather for a city.")
    def get_weather(self, city: str) -> str:
        params = urlencode({"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
        try:
            with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{params}", timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
            return f"{data['name']}: {data['weather'][0]['description']}, {data['main']['temp']} C."
        except Exception as exc:
            return f"Weather API error: {exc}"


# Load only this folder's .env file and create a Semantic Kernel instance.
def create_kernel() -> Kernel:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    kernel = Kernel()
    client = AsyncOpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])
    kernel.add_service(OpenAIChatCompletion(ai_model_id=os.environ["AZURE_OPENAI_DEPLOYMENT"], async_client=client, service_id="foundry-chat"))
    kernel.add_plugin(UtilityPlugin(), plugin_name="Utility")
    return kernel


# Run a tool manually through Semantic Kernel, then summarize with a prompt.
async def main() -> None:
    kernel = create_kernel()
    question = input("Ask math or weather question: ").strip() or "Calculate 18 * 7"
    lowered = question.lower()

    if "weather" in lowered:
        city = question.split(" in ")[-1].strip(" ?.") if " in " in lowered else "Delhi"
        tool_result = await kernel.invoke(plugin_name="Utility", function_name="get_weather", city=city)
    elif "calculate" in lowered:
        expression = lowered.replace("calculate", "").strip()
        tool_result = await kernel.invoke(plugin_name="Utility", function_name="calculator", expression=expression)
    else:
        tool_result = "No tool needed."

    answer = await kernel.invoke_prompt(
        "Answer the user question using this tool result.\nQuestion: {{$question}}\nTool result: {{$tool_result}}",
        arguments=KernelArguments(question=question, tool_result=str(tool_result)),
    )
    print("\nAgent:", answer)


if __name__ == "__main__":
    asyncio.run(main())

