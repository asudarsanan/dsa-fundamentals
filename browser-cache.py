class Session:
    def __init__(self,url,next=None,prev=None):
        self.url = url
        self.next = next
        self.prev = prev

class BrowserHistory(object):

    def __init__(self, homepage):
        """
        :type homepage: str
        init the head and tail
        """
        
        self.homepage = homepage
        ss = Session(self.homepage)
        self.head = ss
        self.tail = ss
        self.onscreen = ss 

    def visit(self, url):
        """
        :type url: str
        :rtype: None

        point the current tail to the new session and increment the length
        """
        new_session = Session(url)
        current = self.onscreen
        current.next = new_session
        new_session.prev = current
        self.onscreen = new_session
        self.tail = new_session

    def back(self, steps):
        """
        :type steps: int
        :rtype: str
        if steps > length of the history, return else to homepage. else rutrn the current afrter moving back
        """
        
        current = self.onscreen
        i = 0
        while steps>0 and current:
            if current == self.head:
                self.onscreen = self.head
                return self.head.url
            elif not current.prev:
                self.onscreen = self.homepage
                return self.homepage
            elif i == steps:
                self.onscreen = current
                return current.url
            current = current.prev
            i +=1
        return self.homepage


    def forward(self, steps):
        """
        :type steps: int
        :rtype: str
        """
        current = self.onscreen
        i = 0
        while steps > 0 and current:
            if not current.next:
                self.onscreen = self.tail
                return self.tail.url
            elif i == steps:
                self.onscreen = current
                return current.url
            else:
                current = current.next
                i+=1
        self.onscreen = self.tail
        return self.tail.url
        


# Your BrowserHistory object will be instantiated and called as such:
# obj = BrowserHistory(homepage)
# obj.visit(url)
# param_2 = obj.back(steps)
# param_3 = obj.forward(steps)