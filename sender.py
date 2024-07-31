import os, socket, time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(),22222))
server.listen(5)

print("HOST: ", server.getsockname())

client, address = server.accept()

file_name = input("File Name : ")
file_size = os.path.getsize(file_name)


client.send(file_name.encode())
client.send(str(file_size).encode())

with open(file_name, "rb") as file:
    c = 0

    start_time = time.time()
    while c <= file_size:
        data = file.read(1024)
        if not (data):
            break
        client.sendall(data)
        c += len(data)

    end_time = time.time()

print('File transfer complete. total time: ', end_time-start_time)
server.close()