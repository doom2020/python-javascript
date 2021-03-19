import time
import random
import gevent
from gevent import monkey
monkey.patch_all()


def work1():
    for i in range(5):
        time.sleep(random.choice([0.1, 0.7, 0.9, 0.5, 0.3]))
        print(f"work1: {str(i)}")


def work2():
    for i in range(5):
        time.sleep(random.choice([0.1, 0.7, 0.9, 0.5, 0.3]))
        print(f"work2: {str(i)}")


if __name__ == "__main__":
    g1 = gevent.spawn(work1)
    g2 = gevent.spawn(work2)
    # g1.join()
    # g2.join()
    gevent.joinall([g1, g2])
    print("主进程结束")
"""
协程必须要join()阻塞，当前线程结束，协程就结束了
"""
