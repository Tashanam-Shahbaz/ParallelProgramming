import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

# Function to calculate sum of squares in a given range
def sum_of_squares(n_start, n_end):
    return sum(i * i for i in range(n_start, n_end))

# Sequential execution
def sequential_sum_of_squares(n):
    return sum_of_squares(0, n)

# Parallel execution using multiprocessing
def parallel_sum_of_squares(n, num_workers):
    chunk_size = n // num_workers
    futures = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for i in range(0, n, chunk_size):
            futures.append(executor.submit(sum_of_squares, i, min(i + chunk_size, n)))
    
    result = sum(f.result() for f in futures)
    return result

# Use ThreadPoolExecutor for multithreading
def parallel_sum_of_squares_threading(n, num_workers):
    chunk_size = n // num_workers
    futures = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for i in range(0, n, chunk_size):
            futures.append(executor.submit(sum_of_squares, i, min(i + chunk_size, n)))
    
    result = sum(f.result() for f in futures)
    return result

if __name__ == '__main__':

    n = 100000000 # Range of numbers to compute sum of squares
    num_workers = 4  # Number of CPU cores to use in parallel execution

    # Sequential execution timing
    start_time = time.time()
    sequential_result = sequential_sum_of_squares(n)
    end_time = time.time()
    sequential_time = end_time - start_time
    print(f"Sequential result: {sequential_result}")
    print(f"Sequential execution time: {sequential_time:.4f} seconds")

    # Parallel execution timing
    start_time = time.time()
    parallel_result = parallel_sum_of_squares(n, num_workers)
    end_time = time.time()
    parallel_time = end_time - start_time
    print(f"Parallel result: {parallel_result}")
    print(f"Parallel execution time: {parallel_time:.4f} seconds")

    # Threading execution timing
    start_time = time.time()
    threading_result = parallel_sum_of_squares_threading(n, num_workers)
    end_time = time.time()
    threading_time = end_time - start_time
    print(f"Threading result: {threading_result}")
    print(f"Threading execution time: {threading_time:.4f} seconds")

    # Seq vs multi-threading Comparison
    speedup_threading = sequential_time / threading_time
    print(f"Speedup (Sequential vs Threading): {speedup_threading:.2f}x")

    # Seq Vs Multi-process Comparison
    speedup_parallel = sequential_time / parallel_time
    print(f"Speedup (Sequential vs Parallel): {speedup_parallel:.2f}x")

    # Multi-thread Vs MultiProcess Comparison
    speedup_threading_vs_parallel = threading_time / parallel_time
    print(f"Speedup (Threading vs Parallel): {speedup_threading_vs_parallel:.2f}x")



# ### Explanation and Results:

# - **Sequential Execution**: This runs on a single core and computes the sum of squares sequentially. This is the baseline for comparison.

# - **Multiprocessing Execution**: This uses `ProcessPoolExecutor`, which spawns multiple processes to parallelize the computation. Each process works independently, making full use of multiple CPU cores.

# - **Multithreading Execution**: This uses `ThreadPoolExecutor`, which runs threads in parallel. However, due to Python’s **Global Interpreter Lock (GIL)**, multithreading is less efficient for CPU-bound tasks like this one because only one thread can execute Python bytecode at a time.

# ### Observations:
# - **Sequential Execution Time**: 13.7748 seconds.
# - **Multiprocessing Execution Time**: 4.5739 seconds (a significant speedup).
# - **Multithreading Execution Time**: 31.8532 seconds (even slower than sequential).

# ### Analysis:

# 1. **Speedup (Sequential vs Parallel)**:
#    - **Speedup = 3.01x** (Multiprocessing outperforms sequential execution by 3x).
#    - This is expected, as multiprocessing uses multiple cores and can parallelize CPU-bound tasks efficiently.
   
# 2. **Speedup (Sequential vs Threading)**:
#    - **Speedup = 0.43x** (Multithreading is slower than sequential execution by ~2.3x).
#    - This is due to Python's GIL, which prevents true parallel execution in threads for CPU-bound tasks. Instead of improving performance, it adds overhead.

# 3. **Speedup (Threading vs Parallel)**:
#    - **Speedup = 6.96x** (Multiprocessing is nearly 7x faster than multithreading).
#    - This clearly shows that multiprocessing is the better choice for CPU-bound tasks, while multithreading struggles due to the GIL.

# ### Additional Observation:
# - **Multiprocessing**: Since each process runs in a separate memory space and has its own Python interpreter, the GIL doesn't limit multiprocessing. This allows true parallelism on multiple CPU cores.
  
# - **Multithreading**: Despite running multiple threads, the GIL only allows one thread to run at a time for CPU-bound tasks. This makes it much less effective for parallelism in computational tasks like sum of squares.

# ### Conclusion:
# - **For CPU-bound tasks**, **multiprocessing** is the clear winner over **multithreading**. Multithreading introduces overhead without improving performance due to the GIL.
  
# - The comparison shows that for tasks involving heavy computation (like the sum of squares), **multiprocessing** results in significant speedup, whereas **multithreading** can even be slower than sequential execution.

