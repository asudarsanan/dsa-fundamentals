
from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []

        def dfs(i,current,total):
            if total == target:
                result.append(current.copy())
                return
            if i >= len(candidates) or total > target:
                return
            
            #include untimited i's and try to call dfs to check sum?
            current.append(candidates[i])
            dfs(i,current,total+candidates[i])
            current.pop()
            dfs(i+1,current,total)
    
        dfs(0,[],0)
dd = Solution()
dd.combinationSum([2,5,6,9],9)