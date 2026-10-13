# This file should be run on poppy
# It listens to users' requests send by button gui and executes a script

import socket
import subprocess

HOST = "0.0.0.0"
PORT = 5000

# PODMIENIC NA JAKIKOLWIEK DZIALAJACY SKRYPT
SCRIPT_PATH = "/home/wave.py"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print(f"Listening for commands on port {PORT}...")

while True:
    conn, addr = server.accept()

    with conn:
        print(f"Connected by {addr}")

        message = conn.recv(1024).decode("utf-8").strip()
        print(f"Received: {message}")

        if message == "WAVE":
            print("Executing wave script...")

            try:
                result = subprocess.run(
                    ["python3", SCRIPT_PATH],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    conn.sendall(b"SUCCESS")
                    print("Script executed successfully.")
                    if result.stdout:
                        print(result.stdout)
                else:
                    conn.sendall(b"FAILED")
                    print("Script failed:")
                    print(result.stderr)

            except Exception as e:
                conn.sendall(b"ERROR")
                print(f"Error: {e}")

        else:
            conn.sendall(b"UNKNOWN COMMAND")

server.close()

