#!/usr/bin/env python3
"""
Test script for the Bedrock Agent Exposer endpoint
Usage: python test-exposer-endpoint.py <API_GATEWAY_URL>
Example: python test-exposer-endpoint.py https://abc123.execute-api.us-east-1.amazonaws.com/prod
"""

import requests
import json
import sys

def test_endpoint(api_url):
    """Test the Bedrock Agent exposer endpoint"""
    
    # Ensure the URL ends with /chat
    if not api_url.endswith('/chat'):
        api_url = api_url.rstrip('/') + '/chat'
    
    # Test data
    test_message = {
        "message": "Hello, can you help me with a SQL query to find all products?"
    }
    
    print(f"Testing endpoint: {api_url}")
    print(f"Test message: {json.dumps(test_message, indent=2)}")
    
    # Check if API key is provided
    if len(sys.argv) == 3:
        api_key = sys.argv[2]
    else:
        print("⚠️  Warning: No API key provided. The request may fail.")
        print("Usage: python test-exposer-endpoint.py <API_GATEWAY_URL> <API_KEY>")
        api_key = None
    
    try:
        # Prepare headers
        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['x-api-key'] = api_key
        
        # Make the POST request
        response = requests.post(
            api_url,
            json=test_message,
            headers=headers,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, indent=2)}")
            print("\n✅ Test successful! The endpoint is working correctly.")
        else:
            print(f"Response Body: {response.text}")
            print(f"\n❌ Test failed with status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"\n❌ Failed to parse JSON response: {str(e)}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test-exposer-endpoint.py <API_GATEWAY_URL> [API_KEY]")
        print("Example: python test-exposer-endpoint.py https://abc123.execute-api.us-east-1.amazonaws.com/prod your-api-key")
        sys.exit(1)
    
    api_url = sys.argv[1]
    test_endpoint(api_url)
