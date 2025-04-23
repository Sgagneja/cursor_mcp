import sys
import json

def send_request(request):
    # Send request to server via stdin
    sys.stdout.write(json.dumps(request) + '\n')
    sys.stdout.flush()
    
    # Read response from stdout
    response = sys.stdin.readline()
    return json.loads(response)

# Test request
test_request = {
    "jsonrpc": "2.0",
    "method": "web_search",
    "params": {"query": "test query"},
    "id": 1
}

try:
    response = send_request(test_request)
    print("Server response:", response)
except Exception as e:
    print("Error:", str(e)) 