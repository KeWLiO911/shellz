import os
import requests
from flask import Flask, request, jsonify

# Directory where the server's assets are stored
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

# Prompt the user for the name of the Flask app
app_name = input("Enter the name of the Flask app: ")

# Create a Flask app with the specified name
app = Flask(app_name)

# Prompt the user for the server address and port
server_address = input("Enter the server address: ")
server_port = input("Enter the server port: ")

# Construct the full URL for the server
server_url = f'http://{server_address}:{server_port}/'

def generate_command(server_url):
    """Generate the command to be executed by the client."""
    # Prompt the user for the command to be executed by the client
    command_str = input("Enter the command to be executed by the client: ")

    # Generate the command to be executed by the client
    command = f"""
    import requests
    import os

    # Execute the '{command_str}' command and store the output
    stream = os.popen('{command_str}')
    output = stream.read()

    # Send the output back to the server
    data = {{'result': output}}
    requests.post('{server_url}', json=data)
    """
    return command

@app.route('/', methods=['POST'])
def handle_post_request():
    """Endpoint for handling POST requests."""
    # Retrieve the 'result' field from the request body
    result = request.json['result']

    # Display the result
    print(result)
    return jsonify({})

if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=server_port, debug=True)

    # Enter an infinite loop to accept commands from the user
    while True:
        # Generate the command to be executed by the client
        command = generate_command(server_url)

        # Send the command to the client
        requests.post(server_url, json={'command': command})
