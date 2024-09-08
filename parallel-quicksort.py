import concurrent.futures
import random
import time

def parallel_quicksort(arr, threshold=1000):
    if len(arr) <= 1:
        return arr
    
    def quicksort(subarr):
        if len(subarr) <= 1:
            return subarr
        pivot = subarr[len(subarr) // 2]
        left = [x for x in subarr if x < pivot]
        middle = [x for x in subarr if x == pivot]
        right = [x for x in subarr if x > pivot]
        
        if len(subarr) > threshold:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                left_future = executor.submit(quicksort, left)
                right_future = executor.submit(quicksort, right)
                left = left_future.result()
                right = right_future.result()
        else:
            left = quicksort(left)
            right = quicksort(right)
        
        return left + middle + right
    
    return quicksort(arr)

def sequential_quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return sequential_quicksort(left) + middle + sequential_quicksort(right)

# Test the implementations
if __name__ == "__main__":
    # Generate a large random array
    arr_size = 1_000_000
    arr = [random.randint(1, 1000000) for _ in range(arr_size)]
    
    # Test parallel quicksort
    start_time = time.time()
    sorted_parallel = parallel_quicksort(arr.copy())
    parallel_time = time.time() - start_time
    print(f"Parallel Quicksort took {parallel_time:.2f} seconds")
    
    # Test sequential quicksort
    start_time = time.time()
    sorted_sequential = sequential_quicksort(arr.copy())
    sequential_time = time.time() - start_time
    print(f"Sequential Quicksort took {sequential_time:.2f} seconds")
    
    # Verify results
    print("Arrays sorted correctly:", sorted_parallel == sorted_sequential)
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")