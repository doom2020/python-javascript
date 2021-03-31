import socket

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    message = input("请输入: ")
    s.sendto(message.encode('utf8'), ('127.0.0.1', 9090))
    data = s.recv(1024)
    print("data: %s" % data.decode('utf8'))
