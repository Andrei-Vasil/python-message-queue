import threading, random, time, requests

def pusher():
    x = random.randint(1, 10)
    requests.post('http://localhost:5000/push', data={'item': x})

def pusher_wrapper():
    for _ in range(5000):
        pusher()

def popper():
    requests.get('http://localhost:5000/pop')

def popper_wrapper():
    for _ in range(5000):
        popper()

def main():
    start = time.time()
       
    pusher_thread = threading.Thread(target=pusher_wrapper)
    pusher_thread.start()

    popper_thread = threading.Thread(target=popper_wrapper)
    popper_thread.start()

    pusher_thread.join()
    popper_thread.join()

    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
