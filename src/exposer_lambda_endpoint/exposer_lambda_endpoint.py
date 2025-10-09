import json
import boto3
import os

bedrock_agent = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        # Manejo del evento HTTP desde API Gateway
        body = event.get("body")
        if body and isinstance(body, str):
            body = json.loads(body)
        elif not body:
            body = event

        user_message = body.get("message")
        if not user_message:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Falta el campo 'message' en el body"})
            }

        # Invocar al agente de Bedrock
        response = bedrock_agent.invoke_agent(
            agentId=os.environ["BEDROCK_AGENT_ID"],
            agentAliasId=os.environ.get("BEDROCK_AGENT_ALIAS_ID", "latest"),
            sessionId="chat-session-001",
            inputText=user_message
        )

        # Extraer la respuesta del flujo de eventos
        message = ""
        for event_stream in response["completion"]:
            if "chunk" in event_stream:
                chunk = event_stream["chunk"]["bytes"]
                message += chunk.decode("utf-8")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": message})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
