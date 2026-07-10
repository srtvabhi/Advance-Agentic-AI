from semantic_kernel.functions import KernelArguments

from config.settings import create_kernel
from plugins.change_automation_plugin import ChangeAutomationPlugin


async def run_change_pipeline(change_request: str) -> str:
    kernel = create_kernel()
    kernel.add_plugin(ChangeAutomationPlugin(), plugin_name="ChangeAutomation")

    change_type = await kernel.invoke(
        plugin_name="ChangeAutomation",
        function_name="validate_change_type",
        change_request=change_request,
    )
    standard = await kernel.invoke(
        plugin_name="ChangeAutomation",
        function_name="retrieve_standard",
        change_request=change_request,
    )

    plan = await kernel.invoke_prompt(
        (
            "You are an IT change manager. Build an automation plan using the change type "
            "and retrieved standard. Keep it practical.\n\n"
            "Change request: {{$change_request}}\nChange type: {{$change_type}}\n"
            "Standard:\n{{$standard}}\n\n"
            "Return under 250 words with these headings: approvals, implementation, rollback, validation, communication."
        ),
        arguments=KernelArguments(change_request=change_request, change_type=str(change_type), standard=str(standard)),
    )

    record = await kernel.invoke(
        plugin_name="ChangeAutomation",
        function_name="create_change_record",
        change_type=str(change_type),
        summary=change_request,
    )
    notification = await kernel.invoke(
        plugin_name="ChangeAutomation",
        function_name="send_notification",
        message=f"{change_type}: {change_request}",
    )

    return (
        f"--- Change Type ---\n{change_type}\n\n"
        f"--- Retrieved Standard ---\n{standard}\n\n"
        f"--- Automation Plan ---\n{plan}\n\n"
        f"--- Change Record ---\n{record}\n\n"
        f"--- Notification ---\n{notification}"
    )
