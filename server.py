import struct
import threading
import socket
import random


def handleMessage(data, addr, conn):
    type, sub_type, length, sub_length = struct.unpack('>bbhh', data[:6])
    data_receive = struct.unpack(f'>{length}s', data[6:6 + length])[0].decode()

    if type == 0:  # asking for info about connections
        if sub_type == 0 or sub_type == 2:
            server_string = ""
            for key in servers_connected:
                server_string += servers_connected[key] + ":" + str(key) + "/0"
            conn.send(struct.pack('>bbhh{}s'.format(len(server_string)), 1, 0, len(server_string), 0, server_string.encode()))

        if sub_type == 1:
            client_string = ""
            for key in clients:
                client_string += servers_connected[key] + ":" + str(key) + "/0"
            conn.send(struct.pack('>bbhh{}s'.format(len(client_string)), 1, 0, len(client_string), 0, client_string.encode()))
    if type == 1:  # answer for info about connections
        if sub_type == 0:  # info about servers ex. 127.0.0.1:1234/0...
            data_receive = data_receive.split('/0')
            data_receive.pop((len(data_receive) - 1))
            for add in data_receive:
                add = add.split(':')
                if int(add[1]) not in servers_connected and int(add[1]) != port:
                    servers_connected[int(add[1])] = add[0]
                    print('my servers connected', servers_connected)
                    connect_new_servers(int(add[1]))

        if sub_type == 1:
            data_receive = data_receive.split('\0')
            for add in data_receive:
                add = add.split(':')
                # [127.0.0.1 , 1234]
                if int(add[1]) not in clients:
                    clients[int(add[1])] = add[0]

    if type == 2:  # define username for curr_connection
        if sub_type == 0:  # servers
            if int(addr[1]) not in servers_connected:
                servers_connected[int(addr[1])] = addr[0]
                servers_socket[addr[1]] = conn
                print(f"New connection from server {addr}")
                print('servers connected: ', servers_connected)
                conn.send(f'(127.0.0.1,{port}) approve the connections'.encode())

        if sub_type == 1: #clients
            if data_receive not in clients:
                clients[data_receive] = addr
                client_socket[data_receive] = conn
                print(f"New connection from client {addr}")
                conn.send(f'(127.0.0.1,{port}) approve the connections'.encode())
                threading.Thread(handle_connection(conn, addr)).start()

    if type == 3:
        if sub_type == 0:
            message = data_receive.split(maxsplit=1)
            receiver = message[0]
            sender = list(clients.keys())[list(clients.values()).index(addr)]
            if receiver not in clients:
                for connection in servers_socket:
                    new_mess = sender + " " + data_receive
                    servers_socket[connection].send(struct.pack('>bbhh{}s'.format(len(new_mess)),4, 0,
                                                                len(new_mess), 0, new_mess.encode()))

            else:
                client_socket[receiver].send(f'{sender} :{message[1]}'.encode())

    if type == 4:
        message = data_receive.split(maxsplit=2)
        sender = message[0]
        receiver = message[1]
        if receiver in clients:
            client_socket[receiver].send(f'{sender} :{message[2]}'.encode())

    if type == 5:  #echo message
        conn.send(" ".encode())


def connect_new_servers(new_server_port):
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_conn.bind((host, port))
    server_conn.connect(('127.0.0.1', new_server_port))

    # connect success
    server_add = server_conn.getpeername()
    print('new connection from:', server_add)
    server_conn.send(struct.pack('>bbhh', 2, 0, 0, 0))  # request for connection
    data = server_conn.recv(1024)
    print(data.decode())
    servers_connected[server_add[1]] = server_add[0]
    servers_socket[server_add[1]] = server_conn
    server_conn.send(struct.pack('>bbhh', 0, 0, 0, 0))  # request for servers list
    threading.Thread(target=handle_connection, args=(server_conn, server_add)).start()


def handle_connection(con, addr):
    data = b''
    while True:
        try:

            data = con.recv(1024)
            if not data:  #client close connection
                client_name = list(clients.keys())[list(clients.values()).index(addr)]
                clients.pop(client_name)
                client_socket.pop(client_name)
                break
            handleMessage(data, addr, con)

        except ConnectionResetError:
            break

        except OSError:
            break
    con.close()
    if data:
        print(f"Connection closed with {addr}")



def listen():
    while True:
        print("Waiting for other servers / clients to connect\n")
        conn, add = server.accept()
        threading.Thread(target=handle_connection, args=(conn, add)).start()


host = '127.0.0.1'
print("**Server**")
while True:
    try:
        port = int(input("Please choose port number (between 1000-5000, jumps for thousand): "))
        if 1000 <= port <= 5000 and port % 1000 == 0:
            break
        else:
            print("Port number must be between 1000 and 5000, and a multiple of 1000.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

address = [('127.0.0.1', 1000), ('127.0.0.1', 2000), ('127.0.0.1', 3000), ('127.0.0.1', 4000), ('127.0.0.1', 5000)]
random.shuffle(address)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

clients = {}
servers_connected = {}  # 1000: '127.0.0.1'
client_socket = {}
servers_socket = {}
print("Searching for another servers to connect with..")
for i in range(len(address)):
    try:
        if address[i][1] != port:
            connect_new_servers(address[i][1])
            break
    except ConnectionRefusedError:
        print("There is no servers on the other side")

threading.Thread(target=listen).start()