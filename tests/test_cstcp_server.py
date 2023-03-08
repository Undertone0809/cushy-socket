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

import time
import socket
import random
import unittest
import threading
import warnings

from cushy_socket.tcp import CushyTCPServer


class TestCSTCPServer(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.port = random.randint(20000, 30000)
        self.server = CushyTCPServer('localhost', self.port)

    def tearDown(self):
        if self.server.is_running and self.server.clients:
            self.server.close()

    def test_create_server(self):
        self.assertIsInstance(self.server, CushyTCPServer)

    def test_start_server(self):
        self.server.run()
        self.assertTrue(self.server.is_running)

    def test_stop_server(self):
        self.server.run()
        self.server.close()
        self.assertFalse(self.server.is_running)

    def test_connect_client(self):
        self.server.run()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', self.port))
        client_socket.sendall(b'hello')
        self.assertIsNotNone(self.server.clients)
        client_socket.close()

    def test_handle_listen_from_client(self):
        received_data = []

        def handle_listen_from_client(data):
            received_data.append(data)

        self.server.listen(handle_listen_from_client)

        self.server.run()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', self.port))
        client_socket.sendall(b'hello')
        client_socket.close()

        time.sleep(0.1)
        self.assertEqual(received_data, ['hello'])

    def test_handle_listen_from_client_decorator(self):
        received_data = []

        @self.server.on_message()
        def handle_listen_from_client(data):
            received_data.append(data)

        self.server.run()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', self.port))
        client_socket.sendall(b'hello')
        client_socket.close()

        time.sleep(0.1)
        self.assertEqual(received_data, ['hello'])

    def test_send_to_client(self):
        received_data = []

        def handle_listen_from_client(data):
            received_data.append(data)

        self.server.listen(handle_listen_from_client)

        self.server.run()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', self.port))
        client_socket.sendall(b'hello')

        time.sleep(0.1)
        self.assertEqual(received_data, ['hello'])

        self.server.send(b'to_client')
        time.sleep(0.1)
        self.assertEqual(received_data, ['hello'])
        client_socket.close()


if __name__ == '__main__':
    unittest.main()
