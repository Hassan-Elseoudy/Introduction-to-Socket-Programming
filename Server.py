#!/usr/bin/python3.7

import socket
import os
import threading
import sys

server_path = os.path.dirname(os.path.realpath(__file__)) + "/Server_stuff"
client_path = os.path.dirname(os.path.realpath(__file__)) + "/Client_stuff"
HOST = 'localhost'
PORT = int(sys.argv[1])


def ack_request(client_socket):
    data = client_socket.recv(1024)
    print('Received {}'.format(data))
    client_socket.send('ACK!'.encode())
    return data


def check_file_in_server(file_name):
    for root, dirs, files in os.walk(server_path):
        for file in files:
            if file == file_name:
                return True
    return False


def handle_request(conn):
    data = ack_request(conn)
    data = data.decode()
    if data.split(" ")[0] == "Get":
        status, file = send_file(data.split(" ")[1])
        conn.send(status.encode())
        if file:
            conn.sendall(file)
    elif data.split(" ")[0] == "Post":
        conn.send(("HTTP/1.0 200 OK" + '\r\n').encode())
        temp = conn.recv(4096)
        upload_file(data.split(" ")[1], temp)
    conn.close()


def send_file(file_name):
    flag = check_file_in_server(file_name)
    print(flag)  # to print 200 OK or 404 Not found.
    if flag:
        with open(server_path + '/' + file_name, 'rb') as handle:
            return "HTTP/1.0 200 OK" + '\r\n', handle.read()
    else:
        return "HTTP/1.0 400 Not Found" + '\r\n', None


def upload_file(file_name, data):
    with open(server_path + '/' + file_name, 'wb') as handle:
        handle.write(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, address = s.accept()
        print('Connected by', address)
        client_handler = threading.Thread(
            target=handle_request,
            args=(conn,)
        )
        client_handler.run()
