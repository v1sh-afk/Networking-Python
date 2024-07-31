import os, socket, time
host = input("Enter the host name : ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((host,22222))
    print("Connected successfully")
except:
    print("Unable to connect")
    exit(0)
file_name = client.recv(100).decode()
file_size = client.recv(100).decode()
with open(file_name,"wb") as file:
    c = 0
    start_time = time.time()
    while c <= int(file_size):
        data = client.recv(1024)
        if not (data):
            break
        file.write(data)
        c += len(data)
    end_time = time.time()
print("File transfer complete. total time : ",end_time - start_time)
client.close()