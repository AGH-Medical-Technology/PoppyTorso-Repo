# This file should be run on your laptop while connected to Poppy's hotspot. It sends request to it via sockets

import socket
import threading
import tkinter as tk

# PLACEHOLDER, CHANGE TO MATCH POPPY'S HOTSPOT IP
PI_IP = "10.10.10.1"
PORT = 5000

def send_wave():
    button.config(state="disabled")
    status_label.config(text="Sending WAVE...")

    def communicate():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(65)
                s.connect((PI_IP, PORT))
                s.sendall(b"WAVE")

                response = s.recv(1024).decode("utf-8")

            message = "Response: " + response

        except socket.timeout:
            message = "Error: Connection timed out"

        except OSError as e:
            message = f"Connection error: {e}"

        root.after(0, lambda: update_status(message))

    threading.Thread(target=communicate, daemon=True).start()


def update_status(message):
    status_label.config(text=message)
    button.config(state="normal")


root = tk.Tk()
root.title("Poppy Controller")
root.geometry("350x200")
root.resizable(False, False)

button = tk.Button(
    root,
    text="SEND WAVE",
    font=("Arial", 16),
    width=15,
    height=2,
    command=send_wave
)
button.pack(pady=35)

status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Arial", 10)
)
status_label.pack()

root.mainloop()
