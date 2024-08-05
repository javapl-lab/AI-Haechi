class GlobalCounter:
    def __init__(self):
        self.num = -1

    def counter(self):
        self.num += 1
        return self.num

    def now(self):
        return self.num
