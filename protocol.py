import socket
import struct

import lz4.frame


def send(sock: socket.socket, buffer: bytes) -> None:
    buffer = lz4.frame.compress(buffer)
    packed_len = struct.pack(">L", len(buffer))
    sock.sendall(packed_len + buffer)


def recv_n(sock: socket.socket, n: int):
    buf = b""
    while n > 0:
        data = sock.recv(n)
        if data == b"":
            raise RuntimeError("unexpected connection close")

        buf += data
        n -= len(data)

    return buf


def recv(sock: socket.socket) -> bytes:
    len_buf = recv_n(sock, 4)
    msg_len = struct.unpack(">L", len_buf)[0]
    return lz4.frame.decompress(recv_n(sock, msg_len))
