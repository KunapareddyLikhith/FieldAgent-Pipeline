# FieldAgent: Voice-Driven AI Automation 🚀

An open-source, serverless agentic pipeline designed for field workers, built for the **Build, Ship, Shape: Amazon Developer Hackathon (Alexa+ Track & AWS Builder Mini Challenge)**.

---

## 🏗️ Architecture & Overview
FieldAgent bridges natural human voice commands directly to secure enterprise backend operations. 

[ Field Worker Voice/Text Command ]
│
▼
[ FastAPI Backend ] (Local / AWS Lambda)
│
▼
[ Amazon Bedrock ] (Claude 3.5 Sonnet via Boto3) ──> Intent Parsing & Parameter Extraction
│
▼
[ Model Context Protocol (MCP) & Database ] ──> Amazon RDS (PostgreSQL State Persistence)


---

## 🛠️ Tech Stack
* **Framework:** FastAPI, Uvicorn, Pydantic
* **AI / Agentic Core:** Amazon Bedrock (`anthropic.claude-3-5-sonnet-20240620-v1:0`), Model Context Protocol (MCP) concepts
* **Cloud & Database:** AWS SDK (`boto3`), Amazon RDS / PostgreSQL (with graceful local simulation fallback)
* **License:** MIT License

---

## ⚙️ Local Setup & Installation

Follow these steps to run the FastAPI backend locally:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/KunapareddyLikhith/FieldAgent-Pipeline.git](https://github.com/KunapareddyLikhith/FieldAgent-Pipeline.git)
   cd FieldAgent-Pipeline
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
(Or manually install core packages: pip install fastapi uvicorn boto3 psycopg2-binary pydantic)

Run the FastAPI server:

Bash
python main.py
Test the API:

Open your browser and go to: http://127.0.0.1:8000

Explore interactive API docs: http://127.0.0.1:8000/docs

💡 Key Features
Natural Language Intent Parsing: Uses Amazon Bedrock to extract structured actions and ticket IDs from unstructured field notes.

Resilient Database Layer: Features automatic connection context managers with graceful fallback simulation modes for rapid local development.

Serverless-Ready Architecture: Clean separation of concerns between API routing, LLM service logic, and database persistence.