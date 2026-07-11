def calculate_readiness_score(workflow_description: str) -> str:
    # Creates a simple deterministic readiness scorecard for teaching.
    checks = {
        "security": any(term in workflow_description.lower() for term in ["security", "rbac", "approval"]),
        "observability": any(term in workflow_description.lower() for term in ["observability", "monitoring", "trace"]),
        "rag": "rag" in workflow_description.lower() or "retrieval" in workflow_description.lower(),
        "tools": "tool" in workflow_description.lower() or "ticket" in workflow_description.lower(),
        "scale": any(term in workflow_description.lower() for term in ["scale", "azure", "production"]),
    }
    passed = sum(1 for value in checks.values() if value)
    score = int((passed / len(checks)) * 100)
    lines = [f"Readiness score: {score}/100"]
    for name, value in checks.items():
        status = "PASS" if value else "NEEDS WORK"
        lines.append(f"{name}: {status}")
    return "\n".join(lines)
