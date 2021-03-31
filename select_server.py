import socket
import select
import queue


s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9000))
s.listen(100)

s.setblocking(False)

msg_dic = {}  # key(每个socket连接), value(客户端发来的消息)
inputs = [s]  # 监听所有的socket连接
outputs = []  # 每当一个客户端发来消息添加socket连接,每当处理完一条消息删除一个socket连接

while True:
    print("服务端监听中...")
    readable, writeable, exceptions = select.select(inputs, outputs, inputs)
    for r in readable:
        if r == s:
            # 新的连接
            conn, addr = r.accept()
            print(f"有新的客户端连接ip: {addr[0]}, 端口: {addr[-1]}")
            conn.send("你好,我是服务端".encode('utf8'))
            inputs.append(conn)  # 添加新的socket连接到inputs
            msg_dic[conn] = queue.Queue()  # 创建当前socket的消息队列
        else:
            try:
                # 旧的连接发消息过来了
                data = r.recv(1024).decode('utf8')
                print(f"旧的客户端发来消息: {data}")
                msg_dic[r].put(data)  # 将客户端的消息放到对应的队列中,在writeable中统一处理
                outputs.append(r)  # 当前客户端发来一条消息,就将当前conn添加
            except Exception as e:
                print(f"客户端异常断开: {e}")
                if r in outputs:
                    outputs.remove(r)
                if r in inputs:
                    inputs.remove(r)
                if msg_dic.get(r):
                    del msg_dic[r]
    for w in writeable:
        msg = msg_dic[w].get()  # 获取所有客户端发来的消息
        w.send(f"你发的消息是: {msg}".encode('utf8'))
        outputs.remove(w)  # 处理完当前conn的消息后就要删除
    for e in exceptions:
        # 有异常的conn 删除, inputs, outputs, msg_dict
        if e in outputs:
            outputs.remove(e)
        if e in inputs:
            inputs.remove(e)
        if msg_dic.get(e):
            del msg_dic[e]

