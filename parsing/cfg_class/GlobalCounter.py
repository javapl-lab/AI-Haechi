class GlobalCounter:
    def __init__(self):
        self.num = 0

    def counter(self):
        self.num += 1
        return self.num
