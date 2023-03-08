<h1 align="center">
    cushy-socket
</h1>
<p align="center">
  <strong>A lightweight python socket library. You can create a TCP/UDP connection easily.</strong>
</p>

<p align="center">
    <a target="_blank" href="">
        <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?label=license" />
    </a>
   <a target="_blank" href=''>
        <img src="https://img.shields.io/github/stars/Undertone0809/cushy-socket.svg" alt="github stars"/>
   </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/broadcast-service?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Total"/>
   </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/broadcast-service?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Week"/>
   </a>
</p>


# Features
- send socket message easily
- listen socket message and support ballback
- support sending group messages to clients
- support decorator version listening
- listen topic message and callback


# Usage

```bash
pip install cushy-socket --upgrade 
```

Here are some minimal example programs using the `cushy-socket`: a server that echoes all data that it receives back(servicing only one client), and a client using it.

- Now let's build a easy echo demo.The first example support IPv4 only.

```python
# echo tcp server program
from cushy_socket.tcp import CushyTCPServer

es_tcp_server = CushyTCPServer(host='localhost', port=7777)
es_tcp_server.run()


@es_tcp_server.on_message()
def handle_msg_from_client(msg: str):
    print(f"[server decorator callback] es_tcp_server rec msg: {msg}")
    es_tcp_server.send("hello, I am server")
```

```python
# echo tcp client program
from cushy_socket.tcp import CushyTCPClient

es_tcp_client = CushyTCPClient(host='localhost', port=7777)
es_tcp_client.run()


@es_tcp_client.on_message()
def handle_msg_from_server(msg: str):
    print(f"[client decorator callback] es_tcp_client rec msg: {msg}")


es_tcp_client.send("hello, here is CSTCP client")
```



# TODO
- [ ] support for more lifecycle callbacks
- [ ] optimize the handle of socket closing
- [ ] optimize syntax expressions
- [ ] add UDP server/client support
- [ ] provide more solutions
- [ ] provide more async supports
- [ ] provide more decorator support
- [ ] optimize unittest
- [ ] send and listen topic message

# Contribution
If you want to contribute to this project, you can submit pr or issue. I am glad to see more people involved and optimize it.
