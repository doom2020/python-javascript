import socket


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9000))
    while True:
        info = s.recv(1024)  # 接收的是字节
        print("服务端消息: %s" % info.decode('utf8'))
        msg = input("请输入你想说的: ")
        s.send(msg.encode('utf8'))
        if msg == 'q':
            break
    s.send('q'.encode('utf8'))
    s.close()

