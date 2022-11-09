class Squares():
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    def __iter__(self): return self
    def __next__(self):
        if self.start >= self.stop:
            raise StopIteration
        current = self.start * self.start
        self.start += 1
        return current

iterator = Squares(0, 4)
even = iter(iterator)
print(type(iterator))
for x in iterator:
    print(x)
