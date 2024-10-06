# Conclusion:
# Different concurrency paradigms—threaded, sequential, and multiprocessing—show significant variations in efficiency.

# Threaded Tasks:
# Efficient for I/O-bound operations, completing in ~2.05 seconds by overlapping tasks.

# Sequential Tasks:
# Processed one after another, resulting in ~200.26 seconds, highlighting inefficiency for independent tasks.

# Multiprocessing Tasks:
# Expected to outperform sequential tasks by utilizing multiple CPU cores, ideal for CPU-bound operations.

# Summary:
# Choose concurrency models based on task nature: 
# - Threaded for I/O-bound tasks 
# - Sequential for dependent tasks 
# - Multiprocessing for CPU-bound tasks.
# Consider a hybrid approach for optimal performance in production.

import threading
import multiprocessing
import time

def perform_task(task_num):
    print(f"Starting task {task_num}")
    time.sleep(2)  # Simulate I/O operation
    print(f"Finished task {task_num}")

# Threaded Implementation
def run_threaded_tasks(task_num):
    threads = []
    for i in range(task_num):
        t = threading.Thread(target=perform_task, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("All tasks completed (Threaded)")

def run_process_tasks(task_num):
    processes = []
    for i in range(task_num):
        p = multiprocessing.Process(target=perform_task, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    print("All tasks completed (Process)")
# Sequential Implementation
def run_sequential_tasks(task_num):
    for i in range(task_num):
        perform_task(i)
    print("All tasks completed (Sequential)")

if __name__ == "__main__":

    task_num  = 100
    start_time  = time.time()
    print("Running Threaded Tasks:")
    run_threaded_tasks(task_num)
    print("Time taken: ", time.time() - start_time)

    start_time = time.time()
    print("\nRunning Sequential Tasks:")
    run_sequential_tasks(task_num)
    print("Time taken: ", time.time() - start_time)


    start_time = time.time()
    print("\nRunning MultiPorcess Tasks:")
    run_process_tasks(task_num)
    print("Time taken: ", time.time() - start_time)


