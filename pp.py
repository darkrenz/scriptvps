import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"[*] Received request:\n{request}")

    # Basic HTTP response with echo
    response = """HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
    <title>Simple Echo Server</title>
</head>
<body>
    <h1>Hello, you sent:</h1>
    <pre>{}</pre>
</body>
</html>
""".format(request)

    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def main():
    host = '0.0.0.0'
    port = 8090
    default_host = '0.0.0.0:143'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[*] Listening on {host}:{port}")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
