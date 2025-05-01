import socket
import threading
from queue import Queue
import sys
import os
from tkinter import *
from tkinter import messagebox

class ClientConnection:
    def __init__(self, host='localhost', port=12345):
        self.message_queue = Queue()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        
        if not host:
            host = self.get_server_ip()
        self.connect_to_server(host, port)
        
        if self.connected:
            self.setup_connection()

    def get_server_ip(self):
        """Prompt user for server IP address using a basic Tkinter dialog"""
        root = Tk()
        root.withdraw()  # Hide main window
        
        # Create a simple dialog window
        dialog = Toplevel(root)
        dialog.title("Server IP")
        dialog.geometry("300x100")
        dialog.transient(root)
        dialog.grab_set()
        
        Label(dialog, text="Enter server IP address:").pack(pady=5)
        ip_var = StringVar(value='localhost')
        entry = Entry(dialog, textvariable=ip_var)
        entry.pack(pady=5)
        
        ip_address = ['localhost']  # Use list to store result
        
        def submit():
            ip_address[0] = ip_var.get()
            dialog.destroy()
            
        Button(dialog, text="Connect", command=submit).pack(pady=5)
        
        # Handle window close
        def on_close():
            ip_address[0] = 'localhost'
            dialog.destroy()
            
        dialog.protocol("WM_DELETE_WINDOW", on_close)
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Wait for input
        dialog.wait_window()
        root.destroy()
        return ip_address[0]
        
    def connect_to_server(self, host, port):
        """Attempt to connect to server"""
        try:
            self.client_socket.connect((host, port))
            self.connected = True
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server at {host}:{port}\n{str(e)}")
            self.connected = False
    
    def setup_connection(self):
        def receive_messages():
            while True:
                try:
                    message = self.client_socket.recv(1024).decode()
                    if message:
                        self.message_queue.put(message)
                except:
                    break
                    
        threading.Thread(target=receive_messages, daemon=True).start()
        
    def send_message(self, message):
        try:
            formatted_message = f"Client: {message}"
            self.client_socket.send(formatted_message.encode())
            self.message_queue.put(formatted_message)
        except:
            pass
            
    def get_new_messages(self):
        messages = []
        while not self.message_queue.empty():
            messages.append(self.message_queue.get())
        return messages
