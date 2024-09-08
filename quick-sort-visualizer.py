import random

def quicksort_visualized(arr, lo, hi, depth=0):
    if lo < hi:
        p = partition_visualized(arr, lo, hi, depth)
        quicksort_visualized(arr, lo, p - 1, depth + 1)
        quicksort_visualized(arr, p + 1, hi, depth + 1)

def partition_visualized(arr, lo, hi, depth):
    pivot = arr[hi]
    i = lo - 1
    print(f"{'  ' * depth}Partitioning: {arr[lo:hi+1]}, Pivot: {pivot}")
    
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    print(f"{'  ' * depth}After partition: {arr[lo:hi+1]}")
    return i + 1

def visualize_quicksort(arr):
    print("Original array:", arr)
    quicksort_visualized(arr, 0, len(arr) - 1)
    print("Sorted array:", arr)

# Example usage
random.seed(42)  # for reproducibility
arr = random.sample(range(1, 21), 10)  # 10 random numbers between 1 and 20
visualize_quicksort(arr)