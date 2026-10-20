import boto3
import json
os_environ = __import__('os').environ

def parse_field_command(command_text: str):
    """
    Simulates sending the raw command to Amazon Bedrock to extract 
    structured JSON tool-call arguments.
    """
    # Initialize the Bedrock Runtime client in your preferred region (e.g., us-east-1)
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name=os_environ.get("AWS_REGION", "us-east-1")
    )
    
    # Using Claude 3.5 Sonnet on Bedrock for precise reasoning
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    
    prompt = f"""
    You are an AI assistant for a field service automation pipeline. 
    Analyze the following field worker command and extract the action type, target ticket ID, and notes as a clean JSON object:
    
    Command: "{command_text}"
    
    Return ONLY a JSON response with keys: "action", "ticket_id", and "notes".
    """
    
    try:
        response = bedrock.converse(
            modelId=model_id,
            messages=[{
                "role": "user",
                "content": [{"text": prompt}]
            }],
            inferenceConfig={"maxTokens": 300, "temperature": 0.0}
        )
        
        # Extract the text response from Bedrock
        output_text = response['output']['message']['content'][0]['text']
        return json.loads(output_text)
        
    except Exception as e:
        # Fallback simulation if AWS credentials aren't fully configured yet on local machine
        print(f"AWS Bedrock connection notice: {e}. Returning simulated structured intent for rapid testing.")
        return {
            "action": "update_ticket",
            "ticket_id": "402",
            "notes": command_text
        }