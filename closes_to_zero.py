
from collections import defaultdict


def closest_to_zero(ts) -> int:
    dc = defaultdict(list)  # Use list as the default factory
    
    # Populate dictionary with absolute difference as key, original value as list of values
    for i in ts:
        dif = abs(i)
        dc[dif].append(i)
    
    # Find the minimum absolute difference
    min_abs = min(dc)
    
    # Handle case where multiple values have the same absolute difference (choose the positive one)
    if -min_abs in dc[min_abs]:
        return min_abs  # Return the positive number if both positive and negative are present
    return dc[min_abs][0]  # Otherwise, return the only number

# Example usage:
ts = [2, -1, 1, -2]
print(closest_to_zero(ts))  # Output should be 1