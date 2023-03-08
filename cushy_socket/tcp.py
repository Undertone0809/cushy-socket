# Copyright (c) 2023 Zeeland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/cushy-socket
# Contact Email: zeeland@foxmail.com


from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from typing import List, Callable
import socket
import logging

__all__ = ['CushyTCPClient', 'CushyTCPServer']
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CushyTCPClient:
    def __init__(self, host: str, port: int):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callbacks: List[Callable] = []
        self.is_running = False

    def run(self):
        """
        startup CSTCP Client
        """
        self.sock.connect((self.host, self.port))
        self.is_running = True
        Thread(target=self._recv_thread).start()

    def send(self, msg: str or bytes):
        if type(msg) == str:
            self._send(msg.encode('utf-8'))
        elif type(msg) == bytes:
            self._send(msg)
        else:
            raise Exception("incorrect data type")

    def _send(self, msg: bytes):
        self.sock.sendall(msg)

    def _recv_thread(self):
        while True:
            msg = self.sock.recv(1024).decode('utf-8')
            if not msg:
                self.logger.error("[cushy-socket] Server connection closed.")
                break
            self.logger.info(f"[cushy-socket] Received msg from server: {msg}")

            for callback in self.callbacks:
                callback(msg)

    def listen(self, callback: Callable):
        self.callbacks.append(callback)

    def on_message(self):
        """
        listen socket message using decorator. You can build a listen callback
        program easily.

        example:
        ----------------------------------------------------------------------
        from cushy_socket.tcp import CushyTCPClient

        es_tcp_client = CushyTCPClient(host='localhost', port=7777)
        es_tcp_client.run()


        @es_tcp_client.on_message()
        def handle_msg_from_server(msg: str):
            print(f"[client decorator callback] es_tcp_client rec msg: {msg}")
        ----------------------------------------------------------------------
        """
        def decorator(func):
            self.callbacks.append(func)
            return func

        return decorator

    def close(self):
        self.sock.close()
        self.is_running = False


class CushyTCPServer:
    def __init__(self, host: str, port: int):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = set()
        self.callbacks: List[Callable] = []
        self.is_running = False
        self.executor = ThreadPoolExecutor()

    def run(self):
        """
        startup CSTCP Server
        """
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.is_running = True
        # self.executor.submit(self._accept_thread)
        Thread(target=self._accept_thread).start()

    def _accept_thread(self):
        while True:
            client_sock, client_addr = self.sock.accept()
            self.logger.info(f"[cushy-socket] New client connected: {client_addr}")
            self.clients.add(client_sock)
            self.executor.submit(self._recv_thread, client_sock)

    def _recv_thread(self, sock: socket.socket):
        """
        receive message from connected socket client
        :param sock: client socket
        :return: None
        """
        while True:
            try:
                msg = sock.recv(1024).decode('utf-8')
            except Exception as e:
                self.logger.error(f"[cushy-socket] Error when receiving msg from client: {e}")
                self.clients.remove(sock)
                sock.close()
                break
            if not msg:
                self.logger.info("[cushy-socket] Client connection closed.")
                self.clients.remove(sock)
                sock.close()
                break
            self.logger.info(f"[cushy-socket] Received msg from client: {msg}")
            self.executor.submit(self._callback_thread, msg)

    def send(self, msg: str or bytes, sock: socket.socket = None):
        """
        send message to connected socket. You can choose specify socket client send message
        """
        if sock:
            self._send(msg, sock)
        else:
            for client in self.clients:
                self._send(msg, client)

    def _send(self, msg: str or bytes, sock: socket.socket):
        if type(msg) == str:
            sock.sendall(bytes(msg, encoding='utf-8'))
        elif type(msg) == bytes:
            sock.sendall(msg)
        else:
            raise Exception("Incorrect data type")

    def _callback_thread(self, msg: str):
        for callback in self.callbacks:
            callback(msg)

    def listen(self, callback: Callable):
        self.callbacks.append(callback)

    def on_message(self):
        """
        listen socket message using decorator. You can build a listen callback
        program easily.

        example:
        ----------------------------------------------------------------------
        from cushy_socket.tcp import CushyTCPServer

        es_tcp_server = CushyTCPServer(host='localhost', port=7777)
        es_tcp_server.run()


        @es_tcp_server.on_message()
        def handle_msg_from_client(msg: str):
            print(f"[server decorator callback] es_tcp_server rec msg: {msg}")
            es_tcp_server.send("hello, I am server")
        ----------------------------------------------------------------------
        """
        def decorator(func):
            self.callbacks.append(func)
            return func

        return decorator

    def close(self):
        """
        close tcp server socket. Exit program if there is not connected socket.
        """
        if self.is_running:
            if self.clients:
                for client in self.clients:
                    client.close()
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            else:
                # todo cancel listening and close socket
                pass
            self.is_running = False
        else:
            raise Exception("socket has not open")
