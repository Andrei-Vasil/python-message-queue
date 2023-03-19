import threading, random, time
from queue_lib.multi_threaded_queue import MultiThreadedQueue

def pusher(queue: MultiThreadedQueue):
    x = random.randint(1, 10)
    print(f'pushin {x}')
    queue.push(x)

def popper(queue: MultiThreadedQueue):
    print(f'poppin {queue.pop()}')

def popper_wrapper(queue: MultiThreadedQueue):
    for _ in range(4):
        popper(queue)

def main():
    with MultiThreadedQueue() as queue:
        for _ in range(3):
            pusher(queue)

        popper_thread = threading.Thread(target=popper_wrapper, args=(queue,))
        popper_thread.start()

        time.sleep(0.2)
        pusher(queue)

        popper_thread.join()
