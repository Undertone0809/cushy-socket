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
# Contact Email: zeeland@foxmail.com

from cushy_socket.tcp import CSTCPClient

es_tcp_client = CSTCPClient(host='localhost', port=7777)
es_tcp_client.run()


@es_tcp_client.on_message()
def handle_msg_from_server(msg: str):
    print(f"[client decorator callback] es_tcp_client rec msg: {msg}")


es_tcp_client.send("hello, here is CSTCP client")
