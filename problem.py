from typing import List


def twoSum(nums: List[int], target: int) -> List[int]:
    j = 0
    
    while j < len(nums):
        for i in range (len(nums)):
            if nums[j] + nums[i] == target and j != i:
                return [j,i]
            elif i == len(nums)-1:
                j+=1
            


print(twoSum(nums=[3,4,5,6],target=7))

hashSet = {}