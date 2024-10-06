import multiprocessing
import time
import numpy as np
from multiprocessing import shared_memory



## FALIED 
## NEED TO FIX

# Define matrix multiplication for a subtask
def matrix_multiply_subtask(start_idx, end_idx, matrix_shape, shm_name_matrix, shm_name_rows):
    # Reattach shared memory in the worker process
    shm_matrix = shared_memory.SharedMemory(name=shm_name_matrix)
    matrix = np.ndarray(matrix_shape, dtype=np.float64, buffer=shm_matrix.buf)
    
    shm_rows = shared_memory.SharedMemory(name=shm_name_rows)
    rows = np.ndarray(matrix_shape, dtype=np.float64, buffer=shm_rows.buf)
    
    # Perform matrix multiplication on the slice of rows
    result = np.dot(rows[start_idx:end_idx], matrix.T)  # Multiplying rows[start:end] with matrix.T (transpose)
    
    # Close the shared memory
    shm_matrix.close()
    shm_rows.close()
    
    return result

# Parallel matrix multiplication using multiprocessing.Pool with shared memory
def matrix_multiply_parallel(matrix, rows):
    matrix_shape = matrix.shape
    
    # Create shared memory objects for the matrix and rows
    shm_matrix = shared_memory.SharedMemory(create=True, size=matrix.nbytes)
    shm_rows = shared_memory.SharedMemory(create=True, size=rows.nbytes)
    
    # Copy data to shared memory
    shared_matrix = np.ndarray(matrix_shape, dtype=np.float64, buffer=shm_matrix.buf)
    shared_rows = np.ndarray(matrix_shape, dtype=np.float64, buffer=shm_rows.buf)
    
    np.copyto(shared_matrix, matrix)
    np.copyto(shared_rows, rows)
    
    # Determine chunk size for each process
    n_chunks = 1
    print("Number of CPU cores:", n_chunks)
    chunk_size = matrix_shape[0] // n_chunks
    
    # Prepare arguments for parallel processing
    pool = multiprocessing.Pool(processes=n_chunks)
    tasks = [(i * chunk_size, (i + 1) * chunk_size if i != n_chunks - 1 else matrix_shape[0],
              matrix_shape, shm_matrix.name, shm_rows.name) for i in range(n_chunks)]
    
    # Perform matrix multiplication in parallel
    results = pool.starmap(matrix_multiply_subtask, tasks)
    
    pool.close()
    pool.join()

    # Combine results
    result = np.vstack(results)
    
    # Cleanup shared memory
    shm_matrix.close()
    shm_matrix.unlink()
    shm_rows.close()
    shm_rows.unlink()

    return result

# Sequential matrix multiplication
def matrix_multiply_sequential(matrix, rows):
    return np.dot(rows, matrix.T)

if __name__ == "__main__":
    # Generate large random matrices for matrix multiplication
    matrix_size = 1000  # Matrix size (1000x1000)
    matrix = np.random.rand(matrix_size, matrix_size)
    rows = np.random.rand(matrix_size, matrix_size)

    # Measure sequential execution time
    start_time = time.time()
    result_seq = matrix_multiply_sequential(matrix, rows)
    seq_time = time.time() - start_time
    print(f"Sequential execution time: {seq_time:.4f} seconds")

    # Measure parallel execution time
    start_time = time.time()
    result_par = matrix_multiply_parallel(matrix, rows)
    par_time = time.time() - start_time
    print(f"Parallel execution time: {par_time:.4f} seconds")
