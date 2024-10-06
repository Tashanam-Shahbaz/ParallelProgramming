# Summary of Race Condition Behavior:
# 
# - With Locks:
#   - Only one thread writes to the file, ensuring sequential and consistent output.
#   - Locks prevent concurrent access, maintaining data integrity.
#
# - Without Locks:
#   - Multiple threads write simultaneously, leading to interleaved lines and potential data corruption.
#   - Illustrates a race condition, where unsynchronized access results in unpredictable output.
#
# Conclusion:
# Implementing locks is crucial for managing shared resources in multithreaded applications, 
# preventing race conditions and ensuring reliable data integrity.

import threading
import time
import random
import os

# File to which threads will write
filename = 'race_condition_example_1.txt'

# Number of iterations for each thread
iterations = 10000

# Function to write to file without using locks (introducing a race condition)
def write_to_file_no_lock(thread_id):
    for _ in range(iterations):
        with open(filename, 'a') as f:  # Open file in append mode
            # Simulating a write operation
            f.write(f"Thread {thread_id}: Writing line {random.randint(1, 100)}\n")
            # Simulate some delay to increase the chance of race condition
            time.sleep(random.uniform(0, 0.0001))

# Function to write to file with locks
def write_to_file_with_lock(thread_id, lock):
    for _ in range(iterations):
        with lock:  # Acquire the lock before writing to the file
            with open(filename, 'a') as f:  # Open file in append mode
                # Simulating a write operation
                f.write(f"Thread {thread_id}: Writing line {random.randint(1, 100)}\n")
                # Simulate some delay
                time.sleep(random.uniform(0, 0.0001))

# Remove the file if it exists for a clean run
if os.path.exists(filename):
    os.remove(filename)

# Create threads for the race condition example
num_threads = 10  # Increase the number of threads
threads_no_lock = []
for i in range(num_threads):
    thread = threading.Thread(target=write_to_file_no_lock, args=(i,))
    threads_no_lock.append(thread)
    thread.start()

# Wait for threads to finish
for thread in threads_no_lock:
    thread.join()

# Display contents of the file after race condition
print("Contents of the file after writing without locks:")
with open(filename, 'r') as f:
    contents_no_lock = f.readlines()
    print("".join(contents_no_lock))

# # Remove the file for the next example
# os.remove(filename)
filename = "race_condition_example_2.txt"
# Create a lock
lock = threading.Lock()

# Create threads for the synchronized example
threads_with_lock = []
for i in range(num_threads):
    thread = threading.Thread(target=write_to_file_with_lock, args=(i, lock))
    threads_with_lock.append(thread)
    thread.start()

# Wait for threads to finish
for thread in threads_with_lock:
    thread.join()

# Display contents of the file after writing with locks
print("Contents of the file after writing with locks:")
with open(filename, 'r') as f:
    contents_with_lock = f.readlines()
    print("".join(contents_with_lock))

# # Clean up by removing the file
# os.remove(filename)



