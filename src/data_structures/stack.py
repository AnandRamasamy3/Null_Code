class stack:
    def __init__(self,values=[]):
        self.values=values[:]
        self.pointer=len(values[:])-1
    def empty(self):
        self.values=[]
        self.pointer=-1
    def push(self,data):
        self.values.append(data)
        self.pointer+=1
    def pop(self):
        popped_value=None
        if self.pointer>=0:
            popped_value=self.values[-1]
            self.values.remove(popped_value)
            self.pointer-=1
        return popped_value
    def first(self):
        if len(self.values)>0:
            return self.values[0]
        else:
            return None
    def top(self):
        if len(self.values)>0:
            return self.values[self.pointer]
        else:
            return None
