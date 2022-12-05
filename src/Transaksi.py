
class Transaction(object):
    def __init__(self, id, start, validation, finish):
        super(Transaction, self).__init__()

        self.id = id
        self.startTS = start
        self.validationTS = validation
        self.finishTS = finish
        self.writeVar = []
        self.readVar = []
        
    def __str__(self):
        string = f""
        string = string + (f"id: {self.id}\n")
        string = string + (f"startTS: {self.startTS}\n")
        string = string + (f"validationTS: {self.validationTS}\n")
        string = string + (f"finishTS: {self.finishTS}\n")
        string = string + (f"writeVar: ")
        string = string + self.writeVar.__str__()
        string = string + (f"\nreadVar: ")
        string = string + self.readVar.__str__()

        return string
