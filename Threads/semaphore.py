import threading
import time
import random
semaphore  = threading.Semaphore(3)

def access_data(thread_id):
    semaphore.acquire()
    print(f"Thread {thread_id} is accessing the data")
    time.sleep(random.randint(1, 5))
    print(f"Thread {thread_id} is releasing the data")
    semaphore.release()


threads = []
for i in range(5):
    thread = threading.Thread(target=access_data, args=(i,))
    threads.append(thread)
    thread.start()    

for thread in threads:
    thread.join()


# A Semaphore(3) is initialized, allowing only 3 threads to access the shared resource simultaneously.
# 5 threads are created, but only 3 can access the resource at a time, thanks to the semaphore.
# Once a thread finishes accessing the resource, it releases the semaphore, allowing other threads to proceed.