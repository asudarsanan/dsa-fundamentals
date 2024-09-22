def subsetsWithoutDuplicates(nums):
    subsets, curSet = [], []
    helper(0, nums, curSet, subsets)
    return subsets
def helper(i, nums, curSet, subsets):
    if i >= len(nums):
        subsets.append(curSet.copy())
        return

    # decision to include nums[i]
    curSet.append(nums[i])
    helper(i + 1, nums, curSet, subsets)
    curSet.pop()

    # decision NOT to include nums[i]
    helper(i + 1, nums, curSet, subsets)


subsetsWithoutDuplicates([1,2,3])
"""
Initial call: helper(0, [1,2,3], [], [])

1. Include 1:
   helper(1, [1,2,3], [1], [])
   
   1.1 Include 2:
       helper(2, [1,2,3], [1,2], [])
       
       1.1.1 Include 3:
             helper(3, [1,2,3], [1,2,3], [])
             Add [1,2,3] to subsets
       1.1.2 Exclude 3:
             helper(3, [1,2,3], [1,2], [[1,2,3]])
             Add [1,2] to subsets
   
   1.2 Exclude 2:
       helper(2, [1,2,3], [1], [[1,2,3], [1,2]])
       
       1.2.1 Include 3:
             helper(3, [1,2,3], [1,3], [[1,2,3], [1,2]])
             Add [1,3] to subsets
       1.2.2 Exclude 3:
             helper(3, [1,2,3], [1], [[1,2,3], [1,2], [1,3]])
             Add [1] to subsets

2. Exclude 1:
   helper(1, [1,2,3], [], [[1,2,3], [1,2], [1,3], [1]])
   
   2.1 Include 2:
       helper(2, [1,2,3], [2], [[1,2,3], [1,2], [1,3], [1]])
       
       2.1.1 Include 3:
             helper(3, [1,2,3], [2,3], [[1,2,3], [1,2], [1,3], [1]])
             Add [2,3] to subsets
       2.1.2 Exclude 3:
             helper(3, [1,2,3], [2], [[1,2,3], [1,2], [1,3], [1], [2,3]])
             Add [2] to subsets
   
   2.2 Exclude 2:
       helper(2, [1,2,3], [], [[1,2,3], [1,2], [1,3], [1], [2,3], [2]])
       
       2.2.1 Include 3:
             helper(3, [1,2,3], [3], [[1,2,3], [1,2], [1,3], [1], [2,3], [2]])
             Add [3] to subsets
       2.2.2 Exclude 3:
             helper(3, [1,2,3], [], [[1,2,3], [1,2], [1,3], [1], [2,3], [2], [3]])
             Add [] to subsets
             
"""