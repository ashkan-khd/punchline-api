import asyncio


def func1():
    loop = asyncio.get_event_loop()
    print(hash(loop))
    loop.run_until_complete(asyncio.sleep(1))
    print("func1")

def func2():
    loop = asyncio.get_event_loop()
    print(hash(loop))
    loop.run_until_complete(asyncio.sleep(1))
    print("func2")


def main():
    loop = None
    try:
        # loop = asyncio.new_event_loop()
        print(hash(loop))
        # asyncio.set_event_loop(loop)
        func1()
        func2()
    finally:
        if loop:
            loop.close()


if __name__ == "__main__":
    main()