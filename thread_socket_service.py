import socket
import threading


def handler_connect(sock, addr):
    sock.send(f'你好呀: {addr}'.encode('utf8'))  # 发送字节
    while True:
        msg = sock.recv(1024)  # 接收的是字节
        print("客户端消息: %s" % msg.decode('utf8'))
        if msg.decode('utf8') == 'q':
            break
        sock.send("我是服务端".encode('utf8'))  # 发送字节
    sock.close()
    print("客户端: %s 断开连接了" % addr[0])


if __name__ == "__main__":
    # 创建套接字
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # 绑定ip端口
    s.bind(('0.0.0.0', 9000))
    # 监听
    s.listen(5)
    while True:
        print("服务监听中....")
        sock, addr = s.accept()
        print(f"客户端: {addr} 已接入")
        t = threading.Thread(target=handler_connect, args=(sock, addr))
        t.start()

