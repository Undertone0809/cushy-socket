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

import socket
from cushy_socket.tcp import CushyTCPServer

cushy_tcp_server = CushyTCPServer(host='localhost', port=7777)
cushy_tcp_server.run()


@cushy_tcp_server.on_connected()
def handle_on_connected(sock: socket.socket):
    print(f"[server decorator callback] new client connected.")
    print(sock)


@cushy_tcp_server.on_disconnected()
def handle_on_disconnected(sock: socket.socket):
    print(f"[server decorator callback] a client disconnected.")
    print(sock)


@cushy_tcp_server.on_message()
def handle_msg_from_client(msg: str, socket: socket.socket):
    print(f"[server decorator callback] cushy_tcp_server rec msg: {msg}")
    cushy_tcp_server.send("hello, I am server")
