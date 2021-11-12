laststr=""
initialState=[]
finalState=[]
states=set()
alfabet=set()
tranzitions=[]
table=[]
def createTable():
    table.append([el for el in alfabet])
    for el in states:
        t=[el]
        for _ in range(len(alfabet)):
            t.append('DIE')
        table.append(t)
    table[0].insert(0,'s')
    input=[]

    with open('date.txt') as f:
        for line in  f:
            line = line.split(" ")
            if line.__contains__('s'):
                line=line[1:]
            if line.__contains__('.'):
                line.remove('.')
            start = line[0]
            end = line[2]
            params=line[3][:-1]
            # print(len(params))
            if params=='1-9':
                params=[str(i) for i in range(1,10)]
            elif len(params) > 1:
                params=params.split(',')
            else:
                params=[params]
            for i in range(1,len(table)):
                if table[i][0]==start:
                    for el in params:
                        if el=='':
                            break
                        j=table[0].index(el)
                        table[i][j]=end







x=True


def verifiComplience():
    global x
    if x:
        createTable()
        x=False
    global laststr
    for el in table:
        print(el)
    while True:
        laststr = ""
        cmd = input("Give input")
        if cmd=="exit":
            return

        startIndex = None
        for el in table:
            if initialState[0] == el[0]:
                startIndex = table.index(el)
        j = None

        for c in cmd:
            if not table[0].__contains__(c):
                print("Input not accepted")
                return
            j = table[0].index(c)
            if table[startIndex][j] == 'DIE' and  finalState.__contains__(table[startIndex][0]):
                print("Input  accepted")
                break
            elif table[startIndex][j] == 'DIE' and not finalState.__contains__(table[startIndex][0]):
                print("Input not accepted")
                return
            else:
                for el in table:
                    if el[0] == table[startIndex][j]:
                        startIndex = table.index(el)
                        laststr+=c;
        if finalState.__contains__(table[startIndex][0]) and table[startIndex][j]!='DIE':
            print("Input accepted")


def printMenu():
    print("1 Read from file")#
    print("2 Read from cmd")
    print("3 Multimea starilor")#
    print("4 Alfabetul")#
    print("5 Tranzitiile")#
    print("6 Multimea starilor finale")#
    print("7 Verifica complience")
    print("8 Da secventa cea mai lunga")

def iterateMenu():
    printMenu()
    while True:
        cmd=input("Input command: ")
        if cmd == "1":
            with open("date.txt") as f:
                for line in f:
                    computeLine(line)
        elif cmd == "2":
            pass
        elif cmd == "3":
            print(states)
        elif cmd == "4":
            print(alfabet)
        elif cmd == "5":
            print(tranzitions)
        elif cmd == "6":
            print(finalState)
        elif cmd=="7": verifiComplience()
        elif cmd=="8": print(laststr)
        elif "exit"==cmd:
            return


def computeLine(line):
    line=line.split()
    if len(line)==5:
        if line[0]=='s':
            initialState.append(line[1])
        elif line[3]=='.':
            finalState.append(line[2])
    for i in range(len(line)):
        if line[i]=="->":
            states.add(line[i-1])
            states.add(line[i+1])
    params=line[-1:][0]
    if params.__contains__('-'):
        params=params.split(',')
    else:
        params=params.split("-")
    if params[0].__contains__('-'):
        for i in range(int(params[0].split('-')[0]),int(params[0].split('-')[1])+1):
            alfabet.add(str(i))
    else:
        for el in params:
            alfabet.add(el)
    a=""

    if line.__contains__('s'):
        line=line[1:4]
    else:
        line=line[0:3]
    t=""
    for el in line:
        t+=el
    if not tranzitions.__contains__(t):
        tranzitions.append(t)



def readFromFile():
    iterateMenu()



if __name__ == '__main__':
    readFromFile()