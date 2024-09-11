
class BrowserHistory(object):

    def __init__(self, homepage):
        """
        :type homepage: str
        init the head and tail
        """
        self.hompage = homepage
        self.cache= []
        self.cache.append(self.hompage)
        self.index = 0


    def visit(self, url):
        if self.index != len(self.cache)-1:
            self.cache= self.cache[:self.index+1]
            self.index = len(self.cache)-1
        self.cache.append(url)
        self.index+=1
    

    def back(self, steps):
        if self.index - steps >=0:
            self.index -=steps
            return self.cache[self.index]
        else:
            self.index = 0
            return self.cache[0]
        
    

    def forward(self, steps):
        if self.index + steps <= len(self.cache)-1:
            self.index += steps
            return self.cache[self.index]
        else:
            self.index = len(self.cache)-1
            return self.cache[self.index]


bc = BrowserHistory("google.com")
bc.visit("fb.com")
bc.back(2)
bc.visit("insta.com")
bc.back(2)
print(bc.cache[bc.index])
bc.forward(2)
print(bc.cache[bc.index])
print(bc.cache)