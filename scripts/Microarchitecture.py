import sys, collections

class CircularQueue:
    def __init__(self):
        self.ptr = []
        self.occupancy = 0
        self.head = -1
        self.tail = -1

    #Multiset comparison
    def compare(self, x, y):
        return collections.Counter(x) == collections.Counter(y)

    def setmetaData(self):
        head = tail = -1
        try:
            head = self.ptr.index('H')
        except ValueError:
           pass 
        else:
            try:
                tail = self.ptr.index('T')
            except ValueError:
                print('Head pointer found with no matching tail pointer\n')
                sys.exit()
        self.occupancy = abs(tail - head)
        self.head = head
        self.tail = tail    

    def getValidEntries(self, lst):
        if self.head > self.tail:
           return [lst[i] for i in range(self.tail+1, self.head+1)] 
        else:
            return lst[self.head:self.tail]

class UArch:

    stats = {'LQ': 0, 'SQ': 0}
    recordStats = False
    def __init__(self, cycle):
        self.cycle = cycle
        self.lq = LoadQueue()
        self.sq = StoreQueue()
        self.rob = ROB()

    def __eq__(self, state):
        return self.lq == state.lq and self.sq == state.sq

    def __str__(self):
        return 'Cycle: ' + str(self.cycle) + '\n' + str(self.rob) + '\n' + str(self.lq) + '\n' + str(self.sq)

class LoadQueue(CircularQueue):
    def __init__(self):
        self.sn = []
        self.pc = []
        self.address = []
        self.storeIdx = []   
        super(LoadQueue, self).__init__()

    def __eq__(self, lqLast):
        if self.occupancy == lqLast.occupancy:
           if self.compare(self.getValidEntries(self.pc), lqLast.getValidEntries(lqLast.pc)):
               if self.compare(self.getValidEntries(self.address), lqLast.getValidEntries(lqLast.address)):
                   return True

        return False        

    def __str__(self):
        return 'LQ: ' + str(self.getValidEntries(self.sn)) + '\n' + str(self.getValidEntries(self.pc)) + '\n' + str(self.getValidEntries(self.address))
 
class StoreQueue(CircularQueue):
    def __init__(self):
        self.sn = []
        self.pc = []
        self.address = []
        super(StoreQueue, self).__init__()

    def __eq__(self, sqLast):
       if self.occupancy == sqLast.occupancy: 
           if self.compare(self.getValidEntries(self.pc), sqLast.getValidEntries(sqLast.pc)): #Ordering enforced: f all(x==y for x,y in zip(self.getValidEntries(self.pc), sqLast.getValidEntries(sqLast.pc))):
               if self.compare(self.getValidEntries(self.address), sqLast.getValidEntries(sqLast.address)):
                   return True
           
       return False

    def __str__(self):
        return 'SQ: ' + str(self.getValidEntries(self.sn)) + '\n' + str(self.getValidEntries(self.pc)) + '\n' + str(self.getValidEntries(self.address)) 

class ROB(CircularQueue):
    def __init__(self):
        self.sn = []
        self.pc = []
        self.inst = []
        super(ROB, self).__init__()

    def __str__(self):
        return 'ROB: ' + str(self.getValidEntries(self.sn)) + '\n' + str(self.getValidEntries(self.pc))
