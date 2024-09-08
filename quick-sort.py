def quickSort(arr, lo, hi):
    if lo < hi:
        partitionPoint = partition(arr, lo, hi)
        quickSort(arr, lo, partitionPoint-1)  # Sort left subarray
        quickSort(arr, partitionPoint+1, hi)  # Sort right subarray
    return arr

def partition(arr, lo, hi):
    pivot = arr[lo]  # Choose the first element as pivot
    left = lo + 1
    right = hi
    
    while True:
        # Move left pointer right until we find an element greater than pivot
        while left <= hi and arr[left] <= pivot:
            left += 1
        # Move right pointer left until we find an element less than or equal to pivot
        while right > lo and arr[right] > pivot:
            right -= 1
        
        if left >= right:  # Pointers have crossed
            break
        # Swap elements at left and right pointers
        arr[left], arr[right] = arr[right], arr[left]
    
    # Place pivot in its correct position
    arr[lo], arr[right] = arr[right], arr[lo]
    return right  # Return the pivot's final position

# Example usage
array = [50,25,92,16,76,30,43,54,19]
print(quickSort(array, 0, len(array)-1))