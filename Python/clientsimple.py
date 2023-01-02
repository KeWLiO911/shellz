import ssl
import json
import time
import random
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace these with the actual server address and port
server_address = '<YOUR_SERVER_IP_HERE>'
server_port = '<YOUR_SERVER_PORT_HERE>'

# Construct the full URL for the server
url = f'https://{server_address}:{server_port}/'

while True:
    # Make an HTTPS request to the server
    try:
        response = requests.get(url, verify=True)

        # Check the status code of the response
        if response.status_code != 200:
            logging.warning(f'Received non-200 status code: {response.status_code}')
            time.sleep(30)
            continue

        # Load the response payload as JSON
        payload = response.json()

        # If the payload contains a 'command' field, execute the command
        if 'command' in payload:
            try:
                # Use a restricted execution environment to safely evaluate the command
                result = ast.literal_eval(payload['command'])
                logging.info(f'Executed command: {payload["command"]}')
            except Exception as e:
                # If an exception is raised, send the exception message back to the server
                data = {'exception': str(e)}
                requests.post(url, json=data)
                logging.error(f'Error executing command: {e}')
    except Exception as e:
        # If an error occurs while making the request, log the error and wait for a while before trying again
        logging.error(f'Error making request: {e}')
        time.sleep(60)

    # Wait for a random interval before making the next request
    time.sleep(random.uniform(5, 15))
