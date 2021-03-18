"""
线程池可实现主线程不等待(非阻塞)
可使用with创建线程池(ThreadPoolExecutor实现了上下文管理)无需手动关闭线程池,但是主线程是阻塞的
普通方法创建线程池,shutdown(wait=False)可以实现主线程的非阻塞
as_completed是一个生成器函数
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
import threading
from threading import Lock


def test(value, p_lock):
    time.sleep(random.choice([1, 7, 9, 5, 3]))
    print(f"当前线程: {threading.get_ident()}, value: {value}")
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
    # with ThreadPoolExecutor(max_workers=4) as tp:
    #     task_ls = []
    #     for i in range(7):
    #         task = tp.submit(test, str(i))
    #         task_ls.append(task)
    #         task.add_done_callback(get_result)
    #     for future in as_completed(task_ls):
    #         data = future.result()
    #         print(f"result: {data}")
    tp = ThreadPoolExecutor(max_workers=4)
    p_lock = Lock()
    for i in range(7):
        task = tp.submit(test, str(i), p_lock)
        task.add_done_callback(get_result)  # 添加回调函数,每个线程执行完后执行回调函数
    tp.shutdown(wait=False)  # 设置主线程是否阻塞,阻塞的话就要等所有线程执行完毕再执行主线程,否则,主线程不必等待
    print(f"主线程结束: {threading.get_ident()}")
