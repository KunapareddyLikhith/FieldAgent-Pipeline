import os
from typing import Dict, Any, List

# Local in-memory state tracking to simulate active database persistence
MOCK_DATABASE: List[Dict[str, Any]] = [
    {
        "anomaly_id": 1,
        "node_id": "Node-04",
        "severity_level": "High",
        "description": "Visible hairline fracture on structural load point.",
        "logged_at": "2026-10-21 14:22:00"
    }
]
counter = 2

def log_anomaly(node_id: str, severity: str, description: str) -> Dict[str, Any]:
    """Appends an anomaly log entry to the active state."""
    global counter
    new_entry = {
        "anomaly_id": counter,
        "node_id": node_id or "Unknown-Node",
        "severity_level": severity or "Medium",
        "description": description or "No description provided",
        "logged_at": "2026-10-21 23:30:00"
    }
    MOCK_DATABASE.append(new_entry)
    counter += 1
    return {"message": "Success", "inserted_id": new_entry["anomaly_id"]}

def fetch_history(node_id: str, **kwargs) -> List[Dict[str, Any]]:
    """Filters log history by a specific field node identity string."""
    if not node_id:
        return MOCK_DATABASE
    return [entry for entry in MOCK_DATABASE if entry["node_id"].lower() == node_id.lower()]

def execute_db_command(tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main Execution Router exposed to the API layer.
    Safely maps structural incoming tool names to target processing handlers.
    """
    try:
        if tool_name == "log_anomaly":
            result = log_anomaly(
                node_id=tool_args.get("node_id"),
                severity=tool_args.get("severity"),
                description=tool_args.get("description")
            )
            return {"status": "success", "payload": result}
            
        elif tool_name == "fetch_history":
            result = fetch_history(node_id=tool_args.get("node_id"))
            return {"status": "success", "payload": result}
            
        else:
            return {
                "status": "unsupported_tool",
                "payload": f"The tool target '{tool_name}' is not registered in the pipeline."
            }
            
    except Exception as e:
        return {
            "status": "database_error",
            "payload": f"An execution error occurred in the data engine: {str(e)}"
        }