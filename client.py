import socket
import struct
import time
import threading


def connect(data):
    for add in data:
        add = add.split(':')
        if int(add[1]) not in servers_connected:
            servers_connected[int(add[1])] = add[0]
            threading.Thread(connect_new_servers(int(add[1]))).start()


def connect_new_servers(new_server_port):
    global min_time, curr_connection
    try:
        server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_conn.bind((host, port))
        server_conn.connect(('127.0.0.1', new_server_port))
        print("Try RTT of:",server_conn.getpeername())
        message = ""
        start = time.time()
        server_conn.send(struct.pack('>bbhh{}s'.format(len(message)), 5, 0, len(message), 0, message.encode()))
        data = server_conn.recv(1024)
        done = time.time()
        server_conn.send(struct.pack('>bbhh{}s'.format(len(client_name)), 2, 1, len(client_name), 0, client_name.encode()))
        data = server_conn.recv(1024)
        print('server: ', data.decode())
        elapsed = done - start
        if elapsed < min_time:
            print("Close server connections:", curr_connection.getpeername())
            min_time = elapsed
            curr_connection.close()
            curr_connection = server_conn
            print("New server connections:",curr_connection.getpeername())

        else:
            print("Close server connections:",server_conn.getpeername())
            server_conn.close()
    except ConnectionResetError:
        print("The server is not connected")


def chat(client):
    data = client.recv(1024)
    print(data.decode())
    receiver_name = data.split(maxsplit=1)[0].decode()
    print(f'Start chat with {receiver_name}')
    while True:
        try:
            message = input(f'{client_name} :')
            mess = receiver_name + " " + message
            client.send(struct.pack('>bbhh{}s'.format(len(mess)), 3, 0, len(mess), 0,
                                           mess.encode()))
            if message == 'finish':
                break

            data = client.recv(1024)
            print(data.decode())
            if data.decode() == f'{receiver_name} :finish':
                break

        except ConnectionResetError:
            break


SERVER_IP_ADDRESS = "127.0.0.1"
host = '127.0.0.1'
SERVER_PORT = int(input("Enter server port number: "))
port = int(input("Enter your port number:(e.g 2222) "))
client_name = input("Enter your name: ")
servers_connected = {}
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.bind((host, port))
client_socket.listen()


curr_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
curr_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
curr_connection.bind((host, port))
curr_connection.connect(('127.0.0.1', SERVER_PORT))
message = ""
start = time.time()
curr_connection.send(struct.pack('>bbhh{}s'.format(len(message)), 5, 0, len(message), 0, message.encode()))
datar = curr_connection.recv(1024)
done = time.time()
elapsed = done - start
min_time = elapsed
curr_connection.send(struct.pack('>bbhh{}s'.format(len(client_name)), 2, 1, len(client_name), 0, client_name.encode()))
data = curr_connection.recv(1024)
print('server: ', data.decode())

curr_connection.send(struct.pack('>bbhh', 0, 2, 0, 0))  # request for servers list
data = curr_connection.recv(1024)
type, sub_type, length, sub_length = struct.unpack('>bbhh', data[:6])
data_receive = struct.unpack(f'>{length}s', data[6:6 + length])[0].decode()
data_receive = data_receive.split('/0')
data_receive.pop((len(data_receive) - 1))
threading.Thread(connect(data_receive)).start()
#=connect(data_receive)

print("The server that chosen: ", curr_connection.getpeername())

main = True
conversation = True
while main:

        select = int(input('1.Start Chat\n2.close\n'))
        if select == 1:
            while conversation:
                sec_choose = int(input('1.start chat conversation\n2.Wait for messages\n3.close conversation\n'))
                if sec_choose == 1:
                    message = input('Enter receiver and then the message:(e.x omer how are you?) ')
                    #receiver_name = message.split(maxsplit=1)[0]
                    curr_connection.send(struct.pack('>bbhh{}s'.format(len(message)), 3, 0, len(message), 0,
                                                   message.encode()))
                    print('wait for response..')
                    #data = client_socket.recv(1024)
                    chat(curr_connection)

                if sec_choose == 2:
                    print('wait for Messages..')
                    #data = client_socket.recv(1024)
                    chat(curr_connection)

                if sec_choose == 3:
                    conversation = False


        if select == 2:
            main = False


curr_connection.close()