# Implementasi concurrency control protocol - Simple Locking with X-lock only
import re 

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

    def data(self):
        return self.item
    
    def checkLocker(self):
        return self.lockedBy

    def showData(self):
        print(f"{self.item} <- {self.lockedBy}")


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
        if self.opType != OperationType.abort and self.opType != OperationType.commit:
            print(f"{self.opType}{self.transaction}({self.itemData.item})", end="")
        else:
            print(f"{self.opType}{self.transaction}", end="")

def isInQueue(queue, transaction):
    for q in queue:
        if q.transaction == transaction:
            return True
    return False

def isLockedbyOther(locker, item, transaction):
    for data in locker:
        if data.data() == item:
                return True, data.checkLocker() != transaction
    return False, False

def lockItem(locker, item, transaction):
    flag = False
    for data in locker:
        if data.data() == item:
            data.lock(transaction)
            flag = True
            break
    if not flag:
        locker.append(ItemData(item))
        locker[-1].lock(transaction)
    return locker

def removeLock(locker, transaction):
    return [data for data in locker if data.checkLocker() != transaction]

def grantLock(data, transaction):
    return Operation(OperationType.lock, transaction, data)

def grantUnlock(data, transaction):
    return Operation(OperationType.unlock, transaction, data)

# def printAll(schedule, queue, locker):
#     print("================Schedule===============↓")
#     for s in schedule:
#         s.show()
#     print("=======================================")
#     print("===============Queue===================")
#     for q in queue:
#         q.show()
#     print("=======================================")
#     print("===============Locker==================")
#     for l in locker:
#         l.showData()
#     print("=======================================↑")

def simplelocking(tc):
    s = []
    ops = tc.split(",")
    for op in ops:
        res = re.findall(r'([A-Z])+([1-9][0-9]*)(\(([A-Z]+)\))*', op)
        s.append(Operation(res[0][0], res[0][1], res[0][3]))

    schedule = []
    queue = []
    dataLocker = []

    for op in s:
        if isInQueue(queue, op.transaction):
            queue.append(op)
        elif op.opType != OperationType.commit:
            isLocked, lockedByOther = isLockedbyOther(dataLocker, op.itemData.data(), op.transaction)
            if isLocked and lockedByOther:
                queue.append(op)
            else:
                if not isLocked:
                    dataLocker = lockItem(dataLocker, op.itemData.item, op.transaction)
                    #grant lock
                    schedule.append(grantLock(op.itemData.item, op.transaction))
                # add operation to schedule
                schedule.append(op)
        elif op.opType == OperationType.commit:
            # add operation to schedule
            schedule.append(op)
            # grant unlock for all items
            for data in dataLocker:
                if data.checkLocker() == op.transaction:
                    schedule.append(grantUnlock(data.data(), op.transaction))
            # unlock data
            dataLocker = removeLock(dataLocker, op.transaction)
            # run queue
            newQueue = []
            for i in range(len(queue)):
                if isInQueue(newQueue, queue[i].transaction):
                    newQueue.append(queue[i])
                elif queue[i].opType != OperationType.commit:
                    isLocked, lockedByOther = isLockedbyOther(dataLocker, queue[i].itemData.item, queue[i].transaction)
                    if isLocked and lockedByOther:
                        newQueue.append(queue[i])
                    else:
                        if not isLocked:
                            dataLocker = lockItem(dataLocker, queue[i].itemData.item, queue[i].transaction)
                            #grant lock
                            schedule.append(grantLock(queue[i].itemData.item, queue[i].transaction))
                        # add operation to schedule
                        schedule.append(queue[i])
                else:
                    # add operation to schedule
                    schedule.append(queue[i])
                    # grant unlock
                    for data in dataLocker:
                        if data.checkLocker() == queue[i].transaction:
                            schedule.append(grantUnlock(data.data(), queue[i].transaction))
                    # unlock data
                    dataLocker = removeLock(dataLocker, queue[i].transaction)
            queue = newQueue
        # printAll(schedule, queue, dataLocker)

    if len(queue) > 0:
        return []

    return schedule

TC1 = "R1(X),W2(X),W3(Y),W2(Y),R1(Y),R1(X),C1,C2,C3"
TC2 = "R1(X),W2(X),W2(Z),W3(Y),W1(X),C1,C2,C3"
TC3 = "R1(A),R2(A),R3(B),R1(B),W3(C),W2(C),R1(C),C1,R2(D),W3(B),C3,W2(D),C2"
TC4 = "R1(A),R3(B),R1(B),W3(C),W2(C),R1(C),C1,R2(D),W3(B),C3,W2(D),C2"
TC5 = "R1(X),W2(Y),W2(X),R1(Y),C1,C2"

#  main
if __name__ == "__main__":
    tc = input("Masukkan TC : ")
    schedule = simplelocking(tc)
    if len(schedule) > 0:
        for op in range(len(schedule)):
            schedule[op].show()
            if op != len(schedule)-1:
                print(",", end="")
    else:
        print("There's a deadlock on schedule")