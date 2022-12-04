class Transaction(object):
    def __init__(self, id, start, validation, finish):
        super(Transaction, self).__init__()

        self.id = id
        self.startTS = start
        self.validationTS = validation
        self.finishTS = finish
        self.writeVar = []
        self.readVar = []
        
    def __TS__(self):
        result = ""
        result += ("id: {self.id}\n")
        result +=("startTS: {self.startTS}\n")
        result += ("validationTS: {self.validationTS}\n")
        result += ("finishTS: {self.finishTS}\n")
        result += ("writeVar: \n")
        result += self.writeVar.__TS__()
        result += ("\nreadVar: \n")
        result +=  self.readVar.__TS__()

        return result
