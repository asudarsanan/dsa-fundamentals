class MinStack:

    def __init__(self):
        self.arr = []
        self.minVal = []
        

    def push(self, val: int) -> None:
        if len(self.minVal) == 0:
            self.minVal.append(val)
        elif self.minVal[-1] >= val:
            self.minVal.append(val)
        else:
            self.minVal.append(self.minVal[-1])
            
        if len(self.arr) == 0:
            self.arr.append(val)
        else:
            self.arr.append(val)

    def pop(self) -> None:

        if len(self.arr) == 0:
            return
        else:
            self.minVal.pop()
            self.arr.pop()

    def top(self) -> int:
        if len(self.arr) == 0:
            return
        else:
            val = self.arr[-1]
            return val
        

    def getMin(self) -> int:
        if len(self.arr) == 0:
            return
        else:
            return self.minVal[-1]
        

ms = MinStack()
ms.push(-1)
ms.push(1)
ms.push(-1)
ms.pop()
ms.top()
ms.getMin()
