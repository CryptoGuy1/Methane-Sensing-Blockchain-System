import socket
import requests
import json
import re

# API Configuration
API_ENDPOINT = "http://127.0.0.1:3000/api/assets"
API_KEY = "33f7bc5f-af3b-4267-972f-19aa7c00366c"

def extract_methane_value(sensor_string):
    """
    Extracts the methane value from a string like 'Methane 16.00 ppm'
    Returns float value or None if parsing fails
    """
    try:
        # Use regex to find the floating point number in the string
        match = re.search(r'(\d+\.\d+)', sensor_string)
        if match:
            return float(match.group(1))
        return None
    except Exception as e:
        print(f"Error extracting methane value: {e}")
        return None

def post_to_hyperledger(methane_level):
    """
    Posts methane level data to Hyperledger Fabric REST server
    """
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }
   
    payload = {
        'rawBody': str(methane_level)
    }
   
    try:
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        print(f"Successfully posted to Hyperledger. Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Hyperledger: {e}")
        return False

# Set up server on the Linux PC
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345      # Port to listen on

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Listening on {HOST}:{PORT}...")

try:
    # Accept incoming connection from Raspberry Pi
    client_socket, client_address = server_socket.accept()
    print(f"Connected by {client_address}")

    # Continuous loop to receive data from Raspberry Pi
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break  # Exit if connection is closed
           
            # Decode and process the received data
            sensor_reading = data.decode().strip()
            print(f"Received data: {sensor_reading}")
           
            # Extract methane value from the string
            methane_level = extract_methane_value(sensor_reading)
           
            if methane_level is not None:
                # Post to Hyperledger
                post_success = post_to_hyperledger(methane_level)
                if not post_success:
                    print("Failed to post to Hyperledger, but continuing to listen...")
            else:
                print(f"Could not extract methane value from: {sensor_reading}")
               
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

except KeyboardInterrupt:
    print("\nServer shutdown requested...")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Clean up
    try:
        client_socket.close()
    except:
        pass
    server_socket.close()
    print("Server shutdown complete")
