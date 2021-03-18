"""
进程池锁用Manager的锁(当有数据写入同一文件的时候再上锁,其他逻辑或者IO互不影响的地方不用加锁)
apply_async 的callback说明:每个进程完成后都会执行执行callback(有几个进程就执行多少次callback)
map_async 的callback说明: 所有进程执行完成后执行callback(不管多少个进程只执行一次callback)
进程池主进程只能阻塞,等到所有进程完成后才能结束主进程
"""

from multiprocessing import Pool, Manager
import time
import random
import os


def test(i, p_lock):
    time.sleep(random.choice([0.5, 0.7, 0.9, 1, 0.3]))
    print(f"当前进程pid: {os.getpid()}, PPID: {os.getppid()}")
    return str(i)


def handler_callback(value):
    try:
        print("上锁")
        p_lock.acquire()
        print(f"这是回调的value: {value}")
        with open(r'C:\Users\mi\Desktop\ccc.txt', 'a') as fw:
            fw.write(str(i))
    except Exception as e:
        print(e)
    finally:
        print("解锁")
        p_lock.release()


if __name__ == "__main__":
    print(f"主进程pid: {os.getpid()}, PPID: {os.getppid()}")
    # res_list = []
    p = Pool(4)
    p_lock = Manager().Lock()
    for i in range(10):
        p.apply_async(func=test, args=(i, p_lock), callback=handler_callback)
        # 将进程结果放到列表中get()获取每个结果
        # res_list.append(p.apply_async(func=test, args=(i, p_lock), callback=handler_callback))
        # [i.get() for i in res_list]
    # p.map_async(func=test, iterable=[i for i in range(10)], callback=handler_callback)
    p.close()
    p.join()
    print('over')
