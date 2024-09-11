from typing import List


def groupAnagrams(strs: List[str]) -> List[List[str]]:
    
    output = []
    sortedList = []

    for i in strs:
        sortedList.append(str(''.join(sorted(i))))
    print(sortedList)

    j =0
    i=0
    group = []
    while i < len(strs) and j < len(strs):
        if i < len(strs)-1 and sortedList[j] == sortedList[i]:
            group.append(strs[i])
            sortedList.remove(strs[i])
            strs.remove[strs[i]]
        elif i == len(strs)-1 :
            if sortedList[j] == sortedList[i]:
                group.append(strs[i])
            j+=1
            if group not in output:
                output.append(group)
            group = []
            i=0
        i+=1

    return output
        
        
strs=["act","pots","tops","cat","stop","hat"]

groupAnagrams(strs)