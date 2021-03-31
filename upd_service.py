import socket


s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 9090))

while True:
    data, addr = s.recvfrom(1024)
    print("client: %s, data: %s" % (data.decode('utf8'), addr))
    s.sendto(data, addr)
