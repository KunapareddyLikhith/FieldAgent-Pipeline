import boto3
import json
from typing import Dict, Any

def parse_field_command(raw_text: str) -> Dict[str, Any]:
    """
    Invokes Claude 3.5 Sonnet on Amazon Bedrock via Boto3 to translate
    unstructured field notes into clean JSON tool parameters.
    """
    try:
        # Initialise standard serverless Bedrock runtime connection client
        bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
        
        system_prompt = (
            "You are an Alexa+ enterprise parsing agent. Analyze the user's field text and output "
            "valid JSON matching this exact layout: "
            "{\"tool\": \"log_anomaly\" or \"fetch_history\", \"arguments\": {\"node_id\": \"string\", \"severity\": \"string\", \"description\": \"string\"}, \"speech_response\": \"A clear sentence Alexa will speak back to the user\"}"
        )
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "system": system_prompt,
            "messages": [{"role": "user", "content": raw_text}],
            "temperature": 0.0
        })
        
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0", 
            body=body
        )
        
        response_body = json.loads(response.get("body").read())
        result_text = response_body["content"][0]["text"]
        return json.loads(result_text)
        
    except Exception as e:
        # Graceful fallback architecture stub for local debugging loops
        return {
            "status": "error",
            "tool": "unknown",
            "arguments": {},
            "speech_response": f"System connectivity interruption encountered: {str(e)}"
        }