"""
future的进程池
"""
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import random
from multiprocessing import Manager
import os


def test(value, p_lock):
    time.sleep(random.choice([0.1, 0.7, 0.9, 0.5, 0.3]))
    print(f"当前进程: {os.getpid()}, value: {value}")
    return value


def get_result(future):
    try:
        print("上锁")
        p_lock.acquire()
        with open(r'C:\Users\mi\Desktop\fff.txt', 'a') as fw:
            fw.write(future.result())
        print(f"回调的结果: {future.result()}")
    except Exception as e:
        print(e)
    finally:
        print("解锁")
        p_lock.release()


if __name__ == "__main__":
    pp = ProcessPoolExecutor(max_workers=4)
    p_lock = Manager().Lock()
    for i in range(7):
        task = pp.submit(test, str(i), p_lock)
        task.add_done_callback(get_result)  # 添加回调函数,每个进程执行完后执行回调函数
    pp.shutdown(wait=False)  # 设置主线程是否阻塞,阻塞的话就要等所有线程执行完毕再执行主线程,否则,主线程不必等待
    print(f"主进程结束: {os.getpid()}")
