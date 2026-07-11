def load_sample_events() -> list[dict]:
    # Simulates events that would normally come from Azure Service Bus, Kafka, or RabbitMQ.
    return [
        {"id": "CLM-1001", "type": "insurance_claim", "priority": "high", "region": "US", "amount": 25000},
        {"id": "CLM-1002", "type": "insurance_claim", "priority": "medium", "region": "EU", "amount": 8000},
        {"id": "CLM-1003", "type": "fraud_review", "priority": "critical", "region": "US", "amount": 75000},
        {"id": "CLM-1004", "type": "document_check", "priority": "low", "region": "APAC", "amount": 1200},
        {"id": "CLM-1005", "type": "insurance_claim", "priority": "high", "region": "EU", "amount": 18000},
    ]


def summarize_events(events: list[dict]) -> str:
    # Creates a small deterministic queue summary before the LLM planning steps.
    total = len(events)
    critical = sum(1 for event in events if event["priority"] == "critical")
    high = sum(1 for event in events if event["priority"] == "high")
    regions = sorted({event["region"] for event in events})
    return f"Loaded {total} events. Critical={critical}, High={high}, Regions={', '.join(regions)}."
