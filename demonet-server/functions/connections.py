import asyncio
import os
import socket
import ssl
from time import sleep


class Connections:

    def __init__(self, host, port, use_ssl=True):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.certpath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
        self.certpath = os.path.join(self.certpath, 'certs')
        self.cert = os.path.join(self.certpath, 'zacsucks.local.crt')
        self.privkey = os.path.join(self.certpath, 'zacsucks.local.key')
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(self.cert, self.privkey)
        self.active_connections = []

    def add_connection(self, conn):
        self.active_connections.append(conn)
        print(self.active_connections)

    def remove_connection(self, conn):
        self.active_connections.remove(conn)

    def show_conns(self):
        print(self.active_connections)

    def send_message(self, message):
        for conn in self.active_connections:
            conn.sendall(message.encode('utf-8'))
            print(f"Sending message {message} to socket: {conn}")

    async def handle_connection(self, conn, addr):
        self.add_connection(conn=conn)
        try:
            while True:
                data = await asyncio.to_thread(conn.recv, 1024)
                if not data:
                    break
                print(f"Received data from {addr}: {data.decode('utf-8')}")
                if data == b"Hello World!":
                    await asyncio.to_thread(conn.sendall, b'Howdy!')
                if data == b"Goodbye!":
                    break
        except ConnectionResetError:
            pass
        finally:
            self.remove_connection(conn)
            conn.close()
            print(f"Connection from {addr} closed")

    async def accept_connection(self, ssock):
        return await asyncio.to_thread(ssock.accept)

    async def start_server(self):
        loop = asyncio.get_event_loop()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(('127.0.0.1', self.port))
            sock.listen(5)
            with self.context.wrap_socket(sock, server_side=True) as ssock:
                print('Socket server listening!')
                while True:
                    conn, addr = await self.accept_connection(ssock)
                    asyncio.create_task(self.handle_connection(conn, addr))