# Example 1: I/O-bound Task with Threading

import threading
import time

def perform_task(task_num):
    print(f"Starting task {task_num}")
    time.sleep(2)  # Simulate I/O operation
    print(f"Finished task {task_num}")

threads = []
for i in range(5):
    print()
    t = threading.Thread(target=perform_task, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("All tasks completed")
