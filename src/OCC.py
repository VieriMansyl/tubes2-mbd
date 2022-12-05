from Transaksi import Transaction
import time

def checkFormat(schedule):
    for i in range (len(schedule)):
        temp = schedule[i]
        command = temp[0]

        if  (command == "R" or command == "W" or command == "C"):
            if (command != "C"):
                if (len(temp)!= 3 or (not(temp[1].isnumeric())) or (not(temp[2].isalpha()))):
                    return False
            else:
                if (len(temp)!= 2 or (not(temp[1].isnumeric()))):
                    return False
        else:
            return False

    return True


def validation(x, transaction) -> bool:
    '''
    If for all Ti with TS (Ti) < TS (Tj) either one of the following condition holds:
        • finishTS(Ti) < startTS(Tj)
        • startTS(Tj) < finishTS(Ti) < validationTS(Tj) and the set of data items written by Ti
        does not intersect with the set of data items read by Tj
    '''
    for i in transaction:
        if (i.validationTS == None or i.id == x.id):
            continue
        if (i.validationTS < x.validationTS):
            if(x.startTS == None or i.finishTS < x.startTS):
                pass
            elif((x.startTS < i.finishTS) and (i.finishTS < x.validationTS)):
                for var in i.writeVar:
                    if var in x.readVar:
                        return False
            else:
                return False
        
    return True


def OCC(totalTransaction, schedule):

    print("\nSerial Optimistic Concurrency Control :")

    transactions = []
    for i in range (totalTransaction):
        tx = Transaction(i+1, None,None,None)
        transactions.append(tx)

    #Read Phase
    for i in range (len(schedule)):
        n = int(schedule[i][1])-1
        if (schedule[i][0] == "R"):
            print("Read", schedule[i][2], "in T", end="")
            print(schedule[i][1])
            transactions[n].readVar.append(schedule[i][2])
        elif (schedule[i][0] == "W"):
            print("Write", schedule[i][2], "in T", end="")
            print(schedule[i][1])
            transactions[n].writeVar.append(schedule[i][2])
            if (transactions[n].startTS == None):
                time.sleep(0.1)
                transactions[n].startTS = time.time()

        elif (schedule[i][0] == "C"):
            print("Commit T", end="")
            print(schedule[i][1])
            time.sleep(0.1)
            transactions[n].validationTS = time.time()

            #Validation Phase
            validateResult = validation(transactions[n], transactions)

            # Write Phase
            if (validateResult):
                time.sleep(0.1)
                transactions[n].finishTS = time.time()
                print("Transaksi T", end="")
                print(n+1, "Succes")
            else:
                print("Transaksi T", end="")
                print(n+1, "failed\nAbort")
                return False
    
    return True

    
def main():
    
    print("====|||Serial Optimistic Concurrency Control|||====")
    print()
    totalTransaction = int(input("Total Transaction : "))


    print("Format Schedule : R1X, W1X, C1")
    print("Schedule : ",end="")
    x = str(input())
    schedule = x.split(", ")

    if not(checkFormat(schedule)):
        print("Wrong Format!")
    
    
    else :
        if (OCC(totalTransaction, schedule)):
            print("Validation Succes")

        else :
            print("Validasi Failed")


if __name__ == '__main__':
    main()
