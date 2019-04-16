#!/usr/bin/python3.7

import socket
import os
import sys

client_path = os.path.dirname(os.path.realpath(__file__)) + "/Client_stuff"
server_path = os.path.dirname(os.path.realpath(__file__)) + "/Server_stuff"
HOST = str(sys.argv[1])  # The server's hostname or IP address
PORT = int(sys.argv[2])  # Port number


def is_file(file_name_):  # Check if file is in client folder or not.
    dir_path = client_path
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file == file_name_:
                return True
    return False


def send_file(file_name):  # Check for a file and return its content.
    flag = is_file(file_name)
    if flag:
        with open(client_path + '/' + file_name, 'rb') as handle:
            return handle.read()


def write_file(file_name, data):  # Write a file to client folder.
    with open(client_path + '/' + file_name, 'wb') as handle:
        handle.write(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect through Host and Port
    while 1:
        command = input('Enter the command: ')
        s.sendall(command.encode())  # Send command (GET/POST FILE)
        command_type = command.split(" ")[0]
        file_name = command.split(" ")[1]
        ack = s.recv(4096)  # Receive ack
        if ack:
            status = s.recv(4096).decode()  # Receive status (200 OK or 404 Not found)
            print(status)
            if status.startswith("HTTP/1.0 200 OK"):
                if command_type == "Get":
                    data = s.recv(4096)
                    write_file(file_name, data)
                elif command_type == "Post":
                    s.sendall(send_file(file_name))
