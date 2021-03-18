"""
queue.Queue 和 multiprocessing.Queue区别
前者单个进程内使用
后者多个进程使用(应用处理内部程序),并不适用于多进程部署
queue.Queue属于同步队列
消费者一直保持阻塞状态，有任务来就执行任务(继承多线程重写 run() 方法, 执行 start()方法)
生产者有任务就将任务放到队列中即可
"""
import threading
import queue
import time

QUEUE_MAX_SIZE = 10
q = queue.Queue(maxsize=QUEUE_MAX_SIZE)


class Worker(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.wait_time = 10

    def run(self):
        while True:
            time.sleep(10)
            q_size = self.q.qsize()
            print(f"消费者:当前队列的长度: {q_size}")
            if q_size < 1:
                print(f"消费者:当前队列为空: {q_size}")
                time.sleep(self.wait_time)
                continue
            try:
                task = self.q.get()
                if task == '6':
                    break
                print(f"消费者:task: {task}")
            except queue.Empty as e:
                print(f"消费者:没有任务了: {e}")
                time.sleep(self.wait_time)
                continue
            print(f"消费者:当前任务: {task}")
            self.q.task_done()


class Producer(object):
    def __init__(self, q):
        self.q = q

    def put(self, task):
        q_size = self.q.qsize()
        print(f"生产者: 当前队列长度: {q_size}")
        try:
            self.q.put(task, block=True, timeout=5)
        except queue.Full as e:
            print(f"生产者: 当前队列满了: {e}")
            self.q.put(task, block=True, timeout=None)


if __name__ == "__main__":
    worker = Worker(q)
    worker.start()
    producer = Producer(q)
    producer.put("hello python")
    producer.put("hello c")
    producer.put("hello c++")
    producer.put("hello java")
    producer.put("hello node")
    producer.put("hello python")
    producer.put("hello c")
    producer.put("hello c++")
    producer.put("hello java")
    producer.put("hello node")
    producer.put("hello python")
    producer.put("hello c")
    producer.put("hello c++")
    producer.put("hello java")
    producer.put("hello node")
    producer.put('6')
