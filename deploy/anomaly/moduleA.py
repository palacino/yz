class Class1:
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2

    def to_string(self):
        return '{:4d} {:4d}'.format(self.m1, self.m2)
