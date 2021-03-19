"""
同步调用 执行完test1后执行test2
asyncio(异步调用):test1和test2遇到阻塞IO后就切换相当于协程,程序之前的IO切换
"""
import asyncio


async def test1():
    print("test1 start")
    await asyncio.sleep(1)
    print("test1 end")


async def test2():
    print("test2 start")
    await asyncio.sleep(3)
    print("test2 end")


async def main():
    await asyncio.gather(test1(), test2())


if __name__ == "__main__":
    asyncio.run(main())
