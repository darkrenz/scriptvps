import socket
import threading
import sys
import time

IP = '0.0.0.0'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 80
PASS = ''
BUFLEN = 8196 * 8
TIMEOUT = 60
MSG = 'SSHPLUS'
DEFAULT_HOST = '0.0.0.0:143'
RESPONSE = "HTTP/1.1 200 <font color=\"null\">SSHPLUS</font>\r\n\r\n"

class Server(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.running = False
        self.host = host
        self.port = port
        self.threads = []
        self.threadsLock = threading.Lock()
        self.logLock = threading.Lock()

    def run(self):
        self.soc = socket.socket(socket.AF_INET)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.settimeout(2)
        self.soc.bind((self.host, self.port))
        self.soc.listen(0)
        self.running = True

        try:
            while self.running:
                try:
                    c, addr = self.soc.accept()
                    c.setblocking(1)
                except socket.timeout:
                    continue

                conn = ConnectionHandler(c, self, addr)
                conn.start()
                self.addConn(conn)
        finally:
            self.running = False
            self.soc.close()

    def printLog(self, log):
        with self.logLock:
            print(log)

    def addConn(self, conn):
        with self.threadsLock:
            if self.running:
                self.threads.append(conn)

    def removeConn(self, conn):
        with self.threadsLock:
            self.threads.remove(conn)

    def close(self):
        self.running = False
        with self.threadsLock:
            for c in self.threads:
                c.close()

class ConnectionHandler(threading.Thread):
    def __init__(self, socClient, server, addr):
        threading.Thread.__init__(self)
        self.clientClosed = False
        self.targetClosed = True
        self.client = socClient
        self.client_buffer = ''
        self.server = server
        self.log = f'Conexao: {addr}'

    # Other methods remain unchanged...

def main(host=IP, port=PORT):
    print("\033[0;34m━"*8, "\033[1;32m PROXY SOCKS", "\033[0;34m━"*8, "\n")
    print("\033[1;33mIP:\033[1;32m " + IP)
    print("\033[1;33mPORTA:\033[1;32m " + str(PORT) + "\n")
    print("\033[0;34m━"*10, "\033[1;32m SSHPLUS", "\033[0;34m━\033[1;37m"*11, "\n")
    server = Server(IP, PORT)
    server.start()
    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print('\nParando...')
            server.close()
            break

if __name__ == '__main__':
    main()
