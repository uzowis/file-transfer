# TCP client app to send/receive files using sockets over a network
import socket
import os
import time
import tqdm

print("")
print("********** XendIT File Transfer (Xclient) v1.0 ***********")
print("-Built by Wizzy|techcrest.com - \n\n")
print("+ Select Transfer Operation \n1 -Send File \n2 -Receive File")
operation = input("Operation (Enter 1/2 to send or receive file )># ")

# parameters
SEPARATOR = "<SEPARATOR>"
SERVER_HOST = "192.168.43.150"
SERVER_PORT = 5001
BUFFER_SIZE = 4096


def send_file():
    filename = input("Enter filename: ")
    if filename == 'exit':
        print("Thank you for using XendIT. \nWE LOVE YOU!!!")
        exit()
    filesize = os.path.getsize(filename)
    # create Sockets
    s = socket.socket()
    print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
    time.sleep(3)
    s.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to {SERVER_HOST}")

    # Send file name over to server
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # Progress Bar
    progress = tqdm.tqdm(range(filesize), f"Transfering File ({filename})...", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)

            if not bytes_read:
                print("\nFile Transfer Completed! \n\nEnter Filename to send more files or type 'exit' to quit Xender \n")
                f.close()
                s.close()
                send_file()
                break

            s.sendall(bytes_read)
            progress.update(len(bytes_read))


def receive_file():
    # create Sockets
    s = socket.socket()
    s.bind(("0.0.0.0", SERVER_PORT))
    s.listen(5)
    print(f"Listening for connection at 0.0.0.0:{SERVER_PORT}")

    receiver_socket,receiver_addr = s.accept()
    print(f"Successfully connected to {receiver_addr}:{receiver_socket} \n")
    received = receiver_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)


    # Receive files from the client
    progress = tqdm.tqdm(range(filesize), f"Receiving file ({filename}) from {receiver_addr}.....", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            bytes_read = receiver_socket.recv(BUFFER_SIZE)

            if not bytes_read:
                f.close()
                receiver_socket.close()
                s.close()
                receive_file()
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    print(f"File ({filename}) | {filesize}Bytes received!")


if operation == "1":
    send_file()
elif operation == "2":
    receive_file()
else:
    exit()


