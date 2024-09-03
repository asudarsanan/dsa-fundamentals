from array import array
import sys
import numpy as np

# Define a function to print array details
def print_array_details(arr, description):
    print(description)
    print(f"Array: {arr}")
    print(f"Length: {len(arr)}")
    print(f"Memory Size (bytes): {sys.getsizeof(arr)}")
    
    # Check the type of array and print additional details
    if isinstance(arr, array):
        print(f"Capacity: {arr.buffer_info()[1]} elements")
    elif isinstance(arr, np.ndarray):
        print(f"NumPy Array Memory (nbytes): {arr.nbytes} bytes")
    
    print('-' * 40)

# Create an array of size 10, but only use 4 elements
allocated_array = array('i', [0] * 10)  # Allocated memory for 10 integers
used_array = array('i', [1, 2, 3, 4])   # Only using the first 4 elements
used_array[4:] = array('i',[0]*6)

# Print details of the Python arrays
print_array_details(allocated_array, "Allocated Array (Size 10, Empty):")
print_array_details(used_array, "Used Array (Size 4, Filled):")

# Create a NumPy array with a large allocated size but fewer elements
large_array = np.zeros(10, dtype=int)  # Allocated memory for 10 integers
large_array[:4] = np.array([1, 2, 3, 4])  # Only fill the first 4 elements

large_array2 = np.zeros(10, dtype=int)  # Allocated memory for 10 integers

# Print details of the NumPy array
print_array_details(large_array, "NumPy Array (Size 10, 4 Used):")
print_array_details(large_array2,"This is an empty numpy array with size 10")
