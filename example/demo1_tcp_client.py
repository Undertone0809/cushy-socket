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

from cushy_socket.tcp import CushyTCPClient

cushy_tcp_client = CushyTCPClient(host='localhost', port=7777)
cushy_tcp_client.run()


@cushy_tcp_client.on_connected()
def handle_on_connected():
    print(f"[client decorator callback] connect to server.")


@cushy_tcp_client.on_disconnected()
def handle_on_disconnected():
    print(f"[client decorator callback] server disconnected.")


@cushy_tcp_client.on_message()
def handle_msg_from_server(msg: str):
    print(f"[client decorator callback] cushy_tcp_client rec msg: {msg}")


cushy_tcp_client.send("hello, here is CSTCP client")
cushy_tcp_client.close()
