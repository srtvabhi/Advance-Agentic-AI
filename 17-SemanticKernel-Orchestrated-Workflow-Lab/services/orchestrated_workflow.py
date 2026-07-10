from semantic_kernel.functions import KernelArguments

from config.settings import create_kernel
from plugins.vendor_risk_plugin import VendorRiskPlugin


async def run_vendor_workflow(request: str) -> str:
    kernel = create_kernel()
    kernel.add_plugin(VendorRiskPlugin(), plugin_name="VendorRisk")

    risk = await kernel.invoke(plugin_name="VendorRisk", function_name="classify_vendor", request=request)
    controls = await kernel.invoke(plugin_name="VendorRisk", function_name="retrieve_controls", request=request)

    assessment = await kernel.invoke_prompt(
        (
            "You are a vendor risk analyst. Create a short assessment using the risk classification "
            "and retrieved policy controls.\n\n"
            "Request: {{$request}}\nRisk: {{$risk}}\nControls:\n{{$controls}}\n\n"
            "Return under 220 words: decision, required approvals, missing evidence, and next action."
        ),
        arguments=KernelArguments(request=request, risk=str(risk), controls=str(controls)),
    )

    task = await kernel.invoke(
        plugin_name="VendorRisk",
        function_name="create_approval_task",
        risk_level=str(risk),
        vendor_name="Contoso Insights",
    )

    return f"--- Risk Classification ---\n{risk}\n\n--- Retrieved Controls ---\n{controls}\n\n--- SK Assessment ---\n{assessment}\n\n--- Approval Task ---\n{task}"
