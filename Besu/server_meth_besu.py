import socket
import requests
import json
import re
import datetime

# Besu API Configuration
API_ENDPOINT = "http://127.0.0.1:3002/assets"

def extract_methane_value(sensor_string):
    """
    Extracts the methane value from a string like 'Methane 16.00 ppm'
    Returns an integer value (scaled by 1000) or None if parsing fails
    """
    try:
        match = re.search(r'(\d+\.\d+)', sensor_string)
        if match:
            return int(float(match.group(1)) * 1000)  # Convert to int for Ethereum BigNumber support
        return None
    except Exception as e:
        print(f"Error extracting methane value: {e}")
        return None

def post_to_besu(methane_level):
    """
    Posts methane level data to Hyperledger Besu REST server
    """
    headers = {
        'Content-Type': 'application/json'
    }
   
    payload = {
        'methaneLevel': methane_level,  # Now an integer
        'timestamp': datetime.datetime.utcnow().isoformat()  # Generate ISO timestamp
    }
   
    try:
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        print(f"Successfully posted to Besu. Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Besu: {e}")
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
                # Post to Besu
                post_success = post_to_besu(methane_level)
                if not post_success:
                    print("Failed to post to Besu, but continuing to listen...")
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
