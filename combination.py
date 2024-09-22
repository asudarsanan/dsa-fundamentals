from typing import List

class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        currentComb,combinations = [],[]
        self.bt(1,currentComb,combinations,n,k)
        return combinations

    def bt(self,i,currentComb,combinations,n,k):
        if len(currentComb) == k:
            combinations.append(currentComb.copy())
            return
        if i > n:
            return
        for j in range(i,n+1):
            currentComb.append(j)
            self.bt(j+1,currentComb,combinations,n,k)
            currentComb.pop()


ss = Solution()
ss.combine(4,2)