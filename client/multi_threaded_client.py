import threading, random, time, requests

def pusher():
    x = random.randint(1, 10)
    headers = {
      'Content-Type': 'application/json', 
      'Accept': 'text/plain'
    }
    body = {
        'item': x
    }
    requests.post('http://localhost:5000/push', headers=headers, data=body)

def pusher_wrapper():
    for _ in range(500):
        pusher()

def popper():
    requests.get('http://localhost:5000/pop')

def popper_wrapper():
    for _ in range(500):
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
