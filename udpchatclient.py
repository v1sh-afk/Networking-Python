import socket
import threading

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            if message == b'NICK':
                client.sendto(nickname.encode('ascii'), ('127.0.0.1', 55555))
            else:
                print(message.decode('ascii'))
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.sendto(message.encode('ascii'), ('127.0.0.1', 55555))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
