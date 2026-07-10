from semantic_kernel.functions import KernelArguments

from config.settings import create_kernel
from plugins.hr_policy_plugin import HRPolicyPlugin


async def run_plugin_lab(question: str) -> str:
    kernel = create_kernel()
    kernel.add_plugin(HRPolicyPlugin(), plugin_name="HRPolicy")

    context = await kernel.invoke(
        plugin_name="HRPolicy",
        function_name="search_policy",
        question=question,
    )

    answer = await kernel.invoke_prompt(
        (
            "You are an HR policy assistant. Answer the employee question only from the provided policy context. "
            "Mention when an HR ticket is useful.\n\n"
            "Question: {{$question}}\n\nPolicy context:\n{{$context}}\n\nAnswer with citations:"
        ),
        arguments=KernelArguments(question=question, context=str(context)),
    )

    ticket = await kernel.invoke(
        plugin_name="HRPolicy",
        function_name="create_hr_ticket",
        employee_name="Asha",
        request_summary=question,
    )

    return f"--- Retrieved Policy Context ---\n{context}\n\n--- Semantic Kernel Answer ---\n{answer}\n\n--- Native Plugin Action ---\n{ticket}"
