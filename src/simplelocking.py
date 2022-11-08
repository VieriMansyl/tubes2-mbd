import re 

# Implementasi concurrency control protocol - Simple Locking with X-lock only

# OperationType menampung seluruh jenis operasi pada schedule
class OperationType:
    lock = 'XL'
    unlock = 'UL'
    read = 'R'
    write = 'W'
    commit = 'C'
    abort = 'A'

# ItemData merepresentasikan data yang dipakai oleh transaksi pada schedule
class ItemData:
    def __init__(self, item):
        self.item = item
        self.lockedBy = None
    
    def lock(self, t):
        self.lockedBy = t
    
    def checkLock(self):
        return self.lockedBy

    def unlock(self):
        self.lockedBy = None


# ReadOperation bertujuan untuk membaca string operasi menjadi class Operation
class ReadOperation:
    def __init__(self, operation):
        op = re.findall(r'([A-Z])+([1-9][0-9]*)(\(([A-Z])\))*', operation)
        self.opType = op[0]
        self.transaction= op[1]
        if self.opType != OperationType.abort and self.opType != OperationType.commit :
            self.itemdata = ItemData(op[3])
        else :
            self.itemdata = None


# membaca file txt
def readTxt(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines[0].split(",")



if __name__ == "__main__":
    # membaca file txt yang berisi schedule
    file = input("Masukkan nama file (.txt): ")
    schedule = readTxt(file + '.txt')
    for operation in schedule:
        op = re.findall(r'([A-Z])+([1-9][0-9]*)(\(([A-Z])\))*', operation)[0]
        print(f'{operation} => {op}')