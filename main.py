from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from bedrock_service import parse_field_command
from database import init_db, save_ticket_action

# Modern FastAPI lifespan handler (replaces deprecated @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    yield
    # Shutdown logic (if any) can go here

app = FastAPI(title="FieldAgent API", version="1.0", lifespan=lifespan)

class FieldCommandRequest(BaseModel):
    worker_id: str
    command_text: str

@app.get("/")
def read_root():
    return {"status": "FieldAgent Backend is running successfully!", "track": "Alexa+"}

@app.post("/api/v1/process-intent")
def process_field_command(payload: FieldCommandRequest):
    if not payload.command_text:
        raise HTTPException(status_code=400, detail="Command text cannot be empty.")
    
    # 1. Extract structured intent via Bedrock/MCP logic
    structured_intent = parse_field_command(payload.command_text)
    
    # 2. Persist the result (or fallback simulation)
    db_saved = save_ticket_action(payload.worker_id, structured_intent)
    
    return {
        "status": "success",
        "worker_id": payload.worker_id,
        "extracted_intent": structured_intent,
        "database_persisted": db_saved,
        "message": "Successfully processed command, extracted parameters, and updated database state."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)