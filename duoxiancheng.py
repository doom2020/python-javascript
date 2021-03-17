from threading import Thread
import threading
import os
import random
import time


def func1():
    for i in range(3):
        time.sleep(random.randint(1, 2))
        print(f"thread1: {threading.get_ident()}, process:{os.getpid()}, process_father: {os.getppid()}")


def func2():
    for i in range(20, 23):
        time.sleep(random.randint(1, 2))
        print(f"thread2: {threading.get_ident()}, process:{os.getpid()}, process_father: {os.getppid()}")


if __name__ == "__main__":
    print(f"主线程:{threading.get_ident()}开始,process:{os.getpid()}, process_father: {os.getppid()}")
    t1 = Thread(target=func1, args=())
    t2 = Thread(target=func2, args=())
    # t1.setDaemon(True)
    # t2.setDaemon(True)
    t1.start()
    t2.start()
    # t1.join()
    # t2.join()
    print('over')
    print(f"主线程:{threading.get_ident()}结束,process:{os.getpid()}, process_father: {os.getppid()}")


"""
总结
1.只要子线程有join就会阻塞主线程
2.子线程没有join,不是守护线程，主线程结束后,子线程继续执行直到程序执行完毕
3.子线程没有join,是守护线程，主线程结束后，子线程立刻停止执行
4.如果子线程有join,则子线程设置为守护线程是无意义的

进程的也是一样的
"""