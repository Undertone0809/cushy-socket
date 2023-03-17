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
        <img src="https://static.pepy.tech/personalized-badge/broadcast-service?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Total"/>
   </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/cushy-socket?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Week"/>
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

```

```python
# echo tcp client program
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

```



# TODO
- [ ] support for more lifecycle callbacks
- [ ] optimize the handle of socket closing
- [ ] add UDP server/client support
- [ ] provide more async supports
- [ ] provide more decorator support
- [ ] optimize unittest
- [ ] send and listen topic message
- [ ] Add support for SSL/TLS encryption for secure communication.
- [ ] Implement timeout functionality for sending and receiving messages to prevent the blocking of threads.
- [ ] Add support for IPv6 addresses for clients and servers.
- [ ] Implement support for multicast sockets.
- [ ] Allow for the customization of the buffer size used for sending and receiving messages.
- [ ] Implement a mechanism for handling exceptions in the background threads to prevent the entire program from crashing.
- [ ] Provide support for advanced features such as non-blocking sockets, multi-threaded server, and asynchronous I/O using asyncio or Twisted.

# Contribution
If you want to contribute to this project, you can submit pr or issue. I am glad to see more people involved and optimize it.
