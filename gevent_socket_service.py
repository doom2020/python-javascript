import gevent
from gevent import monkey
monkey.patch_all()
import socket


def handler_connect(sock, addr):
    sock.send(f"你好呀: {addr}".encode('utf8'))
    while True:
        msg = sock.recv(1024)
        if msg.decode('utf8') == 'q':
            break
        print("客户端消息: %s" % msg.decode('utf8'))
        sock.send("我是服务端".encode('utf8'))
    sock.close()
    print("客户端: %s 断开连接" % addr[0])


if __name__ == "__main__":
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 9000))
    s.listen(6)
    while True:
        print("服务监听中....")
        sock, addr = s.accept()
        print(f"客户端: {addr} 已接入")
        g = gevent.spawn(handler_connect, sock, addr)
        g.start()
