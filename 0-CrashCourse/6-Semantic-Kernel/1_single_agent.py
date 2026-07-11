import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments


# Load only this folder's .env file and create a Semantic Kernel instance.
def create_kernel() -> Kernel:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    kernel = Kernel()
    client = AsyncOpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])
    kernel.add_service(
        OpenAIChatCompletion(
            ai_model_id=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            async_client=client,
            service_id="foundry-chat",
        )
    )
    return kernel


# Run one semantic prompt as a single agent.
async def main() -> None:
    kernel = create_kernel()
    question = input("Ask a question: ").strip() or "Explain Semantic Kernel in one paragraph."
    result = await kernel.invoke_prompt(
        "You are a concise beginner-friendly assistant. Answer this question:\n{{$question}}",
        arguments=KernelArguments(question=question),
    )
    print("\nAgent:", result)


if __name__ == "__main__":
    asyncio.run(main())

