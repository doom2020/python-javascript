from multiprocessing import Process, Lock
import os
import random
import time


def func1(p_lock):
    for i in range(10):
        time.sleep(random.randint(1, 2))
        print(f"process: {os.getpid()} 上锁, father{os.getppid()}")
        p_lock.acquire()
        try:
            with open(r'C:\Users\mi\Desktop\bbb.txt', 'a') as fw:
                fw.write(str(i) + '\n')
        except Exception as e:
            print(e)
        finally:
            p_lock.release()
            print(f"process: {os.getpid()} 解锁")


def func2(p_lock):
    for i in range(20, 30):
        time.sleep(random.randint(1, 2))
        print(f"process: {os.getpid()} 上锁, father{os.getppid()}")
        p_lock.acquire()
        try:
            with open(r'C:\Users\mi\Desktop\bbb.txt', 'a') as fw:
                fw.write(str(i) + '\n')
        except Exception as e:
            print(e)
        finally:
            p_lock.release()
            print(f"process: {os.getpid()} 解锁")


if __name__ == "__main__":
    print(f"主进程{os.getpid()} 开始,father: {os.getppid()}")
    p_lock = Lock()
    p1 = Process(target=func1, args=(p_lock,))
    p2 = Process(target=func2, args=(p_lock,))
    # p1.daemon = True
    # p2.daemon = True
    p1.start()
    p2.start()
    # p1.join()
    # p2.join()
    print('over')
    print(f"主进程{os.getpid()} 结束,father: {os.getppid()}")

"""
总结
1.只要子进程有join就会阻塞主进程
2.子进程没有join,是守护进程，主进程结束后，子进程立刻停止执行
3.子进程没有join,不是守护进程，主进程结束后,子进程继续执行直到程序执行完毕
4.如果子进程有join,则子进程设置为守护进程是无意义的

线程的也是一样的
"""


