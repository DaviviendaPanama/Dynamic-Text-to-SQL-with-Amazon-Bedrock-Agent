# Bedrock Agent Exposer Endpoint

This document describes the new Lambda function that exposes the Bedrock Agent as a REST API endpoint.

## Overview

The `exposer_lambda_endpoint` is a Lambda function that provides a REST API interface to interact with the Bedrock Agent. It accepts POST requests with a message and returns the agent's response.

## Architecture

```
Client -> API Gateway -> Lambda Function -> Bedrock Agent -> Response
```

## Files Added

### Lambda Function Code
- `src/exposer_lambda_endpoint/exposer_lambda_endpoint.py` - Main Lambda function
- `src/exposer_lambda_endpoint/__init__.py` - Python package init
- `src/exposer_lambda_endpoint/openapi.json` - OpenAPI specification

### CDK Infrastructure
- Updated `lib/agent-stack.ts` with:
  - New IAM role for Bedrock Agent access
  - Lambda function definition
  - API Gateway setup
  - CORS configuration

## Deployment

1. **Build the CDK stack:**
   ```bash
   npm run build
   ```

2. **Deploy the stack:**
   ```bash
   cdk deploy
   ```

3. **Get the API Gateway URL:**
   After deployment, the stack will output the API Gateway URL. Look for:
   ```
   Outputs:
   AgentStack.ApiGatewayUrl = https://abc123.execute-api.us-east-1.amazonaws.com/prod
   ```

## API Usage

### Endpoint
```
POST https://your-api-gateway-url/chat
```

### Request Format
```json
{
  "message": "Your message to the Bedrock Agent"
}
```

### Response Format
```json
{
  "reply": "Agent's response"
}
```

### Example Request
```bash
curl -X POST https://your-api-gateway-url/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me with a SQL query?"}'
```

### Example Response
```json
{
  "reply": "Hello! I'd be happy to help you with SQL queries. What would you like to know?"
}
```

## Testing

Use the provided test script:

```bash
python test-exposer-endpoint.py https://your-api-gateway-url
```

## IAM Permissions

The Lambda function has the following IAM permissions:
- `bedrock-agent-runtime:InvokeAgent` - To invoke the Bedrock Agent
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents` - For CloudWatch logging

## Environment Variables

The Lambda function uses these environment variables:
- `BEDROCK_AGENT_ID` - Automatically set to the deployed agent's ID
- `BEDROCK_AGENT_ALIAS_ID` - Set to "latest"

## Error Handling

The endpoint returns appropriate HTTP status codes:
- `200` - Success
- `400` - Bad request (missing message field)
- `500` - Internal server error

## CORS

The API Gateway is configured with CORS to allow requests from any origin with standard headers.

## Security Considerations

- The API Gateway is public by default
- Consider adding authentication (API keys, Cognito, etc.) for production use
- The Lambda function only has permissions to invoke the specific Bedrock Agent

## Troubleshooting

1. **Check CloudWatch Logs** for the Lambda function
2. **Verify API Gateway** is deployed and accessible
3. **Ensure Bedrock Agent** is properly configured and accessible
4. **Check IAM permissions** for the Lambda execution role

## Next Steps

For production use, consider:
- Adding authentication and authorization
- Implementing rate limiting
- Adding request/response logging
- Setting up monitoring and alerting
- Implementing input validation and sanitization
