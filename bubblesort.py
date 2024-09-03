import time
import random

def bubbleSort(arr):
    start_time = time.time()
    i = 0
    while i < len(arr):
        j = 0
        while j < len(arr)-1-i:
            if arr[j] > arr[j+1]:
                tmp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = tmp
            j += 1
        i += 1
    end_time = time.time()
    return arr, end_time - start_time

def bubbleSortImproved(arr):
    start_time = time.time()
    i = 0
    swapped = True
    while i < len(arr) and swapped:
        j = 0
        swapped = False
        while j < len(arr)-1-i:
            if arr[j] > arr[j+1]:
                tmp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = tmp
                swapped = True
            j += 1
        i += 1
    end_time = time.time()
    return arr, end_time - start_time

def run_sort_test(sort_func, arr):
    arr_copy = arr.copy()
    sorted_arr, time_taken = sort_func(arr_copy)
    return time_taken

# Generate a larger random array
array_size = 10000
test_array = [random.randint(1, 10000) for _ in range(array_size)]

# Number of trials
num_trials = 5

# Run multiple trials
bubble_times = []
improved_bubble_times = []

for _ in range(num_trials):
    bubble_times.append(run_sort_test(bubbleSort, test_array))
    improved_bubble_times.append(run_sort_test(bubbleSortImproved, test_array))

# Calculate average times
avg_bubble_time = sum(bubble_times) / num_trials
avg_improved_bubble_time = sum(improved_bubble_times) / num_trials

print(f"Array size: {array_size}")
print(f"Number of trials: {num_trials}")
print(f"Average bubbleSort time: {avg_bubble_time:.6f} seconds")
print(f"Average bubbleSortImproved time: {avg_improved_bubble_time:.6f} seconds")
print(f"Improvement factor: {avg_bubble_time / avg_improved_bubble_time:.2f}x")



