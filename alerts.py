#Alerts Class
class Alert(): #Container Class
    def __init__(self, value=-1):
        self.value = value
        self.weight = -1;

    def __eq__(self, other):
        return (self.weight == other.weight)

    def __lt__(self, other):
        return (self.weight < other.weight)

    def __gt__(self, other):
        return (self.weight > other.weight)

class Overbought(Alert):
    def __init__(self, value=80):
        Alert.__init__(self)
        self.weight = 4         #Overbought Weight = 4

class RsiHigh(Alert):
    def __init__(self):
        Alert.__init__(self, value=70)
        self.weight = 3         #High RSI Weight = 3

class RsiNormal(Alert):
    def __init__(self):
        Alert.__init__(self)
        self.weight = 2         #Normal RSI = 2

class RsiLow(Alert):
    def __init__(self):
        Alert.__init__(self)
        self.weight = 1         #Low RSI = 1

class Oversold(Alert):
    def __init__(self):
        Alert.__init__(self)
        self.weight = 0         #Oversold = 0
