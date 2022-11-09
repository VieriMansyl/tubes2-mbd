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
    
    def checkLocker(self):
        return self.lockedBy

    def unlock(self):
        self.lockedBy = None


# Operation bertujuan untuk membaca suatu string operasi menjadi class Operation
class Operation:
    def __init__(self, opType, transaction, data):
        self.opType = opType                    # Operation Type
        self.transaction= int(transaction)      # Transaction ID
        if self.opType == OperationType.abort or self.opType == OperationType.commit :
        # mengecek apakah operasi merupakan abort atau commit
            self.itemData = None
        else :
            self.itemData = ItemData(data)
    
    
    def show(self):
        print(f"{self.opType}{self.transaction}({self.itemData.item})")


# membaca file txt
def readTxt(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines[0].split(",")


def isWaitingLock(queue, transaction):
    for q in queue:
        if transaction == q.itemData.lockedBy:
            return True
    return False


if __name__ == "__main__":
    # membaca file txt yang berisi schedule
    file = input("Masukkan nama file (.txt): ")
    li = readTxt(file + '.txt')
    s = []      # schedule awal
    for operation in li:
        res = re.findall(r'([A-Z])+([1-9][0-9]*)(\(([A-Z]+)\))*', operation)
        s.append(Operation(res[0][0], res[0][1], res[0][3]))
    
    schedule = []   # schedule final
    listOfData = [] # list of data yang digunakan pada schedule
    queue = []      # queue untuk menentukan transaksi mana yang akan dijalankan apabila terjadi queue

    for op in s:
        # jika operasi merupakan READ atau WRITE
        if(op.opType == OperationType.read or op.opType == OperationType.write):
            if op.itemData not in listOfData:
                listOfData.append(op.itemData)

            # mendapat transaksi yang memegang lock dari data
            dataIdx = listOfData.index(op.itemData)
            currentLocker = listOfData[dataIdx].checkLocker()

            # mengecek apakah transaksi pada operasi sedang menunggu lock
            isWaiting = isWaitingLock(queue, op.transaction)

            if(currentLocker == None and not isWaiting):
                op.itemData.lock(op.transaction)
                new_lock = Operation(OperationType.lock, op.transaction, op.itemData.item)
                schedule.append(new_lock)
                schedule.append(op)
                listOfData[dataIdx].lock(op.transaction)            # update lock pada listOfData
            elif(currentLocker == op.transaction and not isWaiting):
                schedule.append(op)
            else:
                queue.append(op)
        
        # jika operasi merupakan COMMIT
        elif(op.opType == OperationType.commit):
            # melakukan unlock pada seluruh data yang sedang digunakan transaksi
            for data in listOfData:
                if data.lockedBy == op.transaction:
                    data.unlock()
                    new_unlock = Operation(OperationType.unlock, op.transaction, data.item)
                    schedule.append(new_unlock)

            # eksekusi operasi yang menunggu lock akibat transaksi yang baru saja melakukan commit
            for q in queue:
                if q.itemData not in listOfData:
                    listOfData.append(q.itemData)
                dataIdx = listOfData.index(q.itemData)
                currentLocker = listOfData[dataIdx].checkLocker()

                # ingat yg di excel
                if(currentLocker == None):
                    q.itemData.lock(q.transaction)
                    new_lock = Operation(OperationType.lock, q.transaction, q.itemData.item)
                    schedule.append(new_lock)
                    schedule.append(q)
                    queue.remove(q)
                    # update lock pada listOfData
                    dataIdx = listOfData.index(q.itemData)
                    listOfData[dataIdx].lock(q.transaction)
                else:
                    continue
    
    for op in schedule:
        op.show()
        print(op.itemData.checkLocker())