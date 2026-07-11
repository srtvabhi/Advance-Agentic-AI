from models.pipeline_models import PipelineState
from services.llm_service import ask_model
from services.queue_service import load_sample_events, summarize_events


def receive_events_node(state: PipelineState) -> PipelineState:
    # Loads sample events to demonstrate queue-based orchestration.
    events = load_sample_events()
    state["events"] = events
    state["queue_summary"] = summarize_events(events)
    return state


def routing_node(state: PipelineState) -> PipelineState:
    # Designs routing rules for each event type and priority.
    state["routing_plan"] = ask_model(
        "You are an enterprise AI routing architect.",
        (
            "Create a routing plan for these queue events. Include priority handling, "
            "event categories, and which worker lane should process each event.\n\n"
            f"Objective: {state['objective']}\n"
            f"Queue summary: {state['queue_summary']}\n"
            f"Events: {state['events']}"
        ),
    )
    return state


def worker_pool_node(state: PipelineState) -> PipelineState:
    # Designs worker pools for distributed event processing.
    state["worker_pool_plan"] = ask_model(
        "You are a distributed systems engineer designing AI worker pools.",
        (
            "Convert the routing plan into worker pool design. Include stateless workers, "
            "stateful tracking, concurrency, and back-pressure handling.\n\n"
            f"Routing plan:\n{state['routing_plan']}"
        ),
    )
    return state


def scaling_node(state: PipelineState) -> PipelineState:
    # Adds production scalability, latency, and cost controls.
    state["scaling_plan"] = ask_model(
        "You are a production AI reliability engineer.",
        (
            "Create a scalability plan for this AI orchestration pipeline. Include autoscaling, "
            "queue depth metrics, cost optimization, latency optimization, and dependency limits.\n\n"
            f"Worker pool plan:\n{state['worker_pool_plan']}"
        ),
    )
    return state


def final_report_node(state: PipelineState) -> PipelineState:
    # Produces the final learner-friendly pipeline summary.
    state["final_report"] = ask_model(
        "You are a technical trainer explaining production AI orchestration.",
        (
            "Create a concise final report for participants. Explain the queue-based pipeline, "
            "routing, workers, scaling, and reliability considerations.\n\n"
            f"Objective: {state['objective']}\n"
            f"Queue summary: {state['queue_summary']}\n"
            f"Routing plan:\n{state['routing_plan']}\n"
            f"Worker pool plan:\n{state['worker_pool_plan']}\n"
            f"Scaling plan:\n{state['scaling_plan']}"
        ),
    )
    return state
