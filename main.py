from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from bedrock_service import parse_field_command
from database import execute_db_command

app = FastAPI(title="Alexa+ FieldAgent Pipeline API")

class VoiceCommandPayload(BaseModel):
    raw_text: str
    operator_id: Optional[str] = "Field-Agent-01"

@app.post("/api/v1/agent/execute")
async def handle_agent_execution(payload: VoiceCommandPayload) -> Dict[str, Any]:
    """
    Primary endpoint mimicking the Alexa+ Agent Skill execution flow.
    Parses natural language and routes execution to system tools.
    """
    if not payload.raw_text.strip():
        raise HTTPException(status_code=400, detail="Command text cannot be empty")
    
    # Step 1: Route unstructured voice text through Bedrock for intent parsing
    parsed_intent = parse_field_command(payload.raw_text)
    
    if parsed_intent.get("status") == "error":
        raise HTTPException(status_code=500, detail="Failed to parse command structure via Bedrock")
        
    tool_name = parsed_intent.get("tool")
    tool_args = parsed_intent.get("arguments", {})
    
    # Step 2: Route structured arguments to our Database Tool Execution Engine
    db_result = execute_db_command(tool_name, tool_args)
    
    return {
        "alexa_response": parsed_intent.get("speech_response"),
        "pipeline_execution": {
            "intent_parsed": tool_name,
            "args_extracted": tool_args,
            "system_status": db_result.get("status"),
            "data": db_result.get("payload")
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
