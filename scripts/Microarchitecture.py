import collections
import enum
import sys

def find_index(lst, condition):
    idx = None
    for i, elem in enumerate(lst):
         if condition(elem):
             return i
    return idx 

class FunctionalUnits(enum.Enum):
    ALU = 0
    ADDRGEN = 1
    DIV = 2
    MUL = 3

class Component(enum.Enum):
    LQ = 0
    SQ = 1
    ROB = 2
    LFB = 3
    HWPREFETCHER = 4
    EXESTATUS = 5
#    IPRF = 6
#    FPRF = 7

# Counting-sort comparison
def compareContent(x, y):
    return collections.Counter(x) == collections.Counter(y)

class CircularQueue:
    def __init__(self):
        self.ptr = [] 
        self.occupancy = 0
        self.head = -1
        self.tail = -1

    def setmetaData(self):
        head = tail = -1
        try:
            head = self.ptr.index('H')
        except ValueError:
           pass 
        else:
            try:
                tail = self.ptr.index('T')
            except ValueError as e:
                raise e
        self.occupancy = abs(tail - head)
        self.head = head
        self.tail = tail    

    def getValidEntries(self, lst):
        if self.head > self.tail:
           return [lst[i] for i in range(self.tail+1, self.head+1)] 
        else:
            return lst[self.head:self.tail]

class UArch:

    def __init__(self, cycle):
        self.cycle_begin = cycle
        self.cycle_end = None
        self.lq = LoadQueue()
        self.sq = StoreQueue()
        self.rob = ROB()
        self.lfb = LineFillBuffer()
        self.hwprefetcher = Prefetcher()
        self.intRegFile = RegisterFile('IntPRF')
        self.fpRegFile = RegisterFile('FpPRF')
        self.executionUnitsBusy = ExecutionUnitsStatus()

    def __eq__(self, state):
        return self.lq == state.lq and \
               self.sq == state.sq and \
               self.rob == state.rob and \
               self.lfb == state.lfb and \
               self.hwprefetcher == state.hwprefetcher and \
               self.executionUnitsBusy == state.executionUnitsBusy

    def compare(self, comptype, state):
        if comptype == Component.LQ:
            return self.lq == state.lq
        elif comptype == Component.SQ:
            return self.sq == state.sq
        elif comptype == Component.ROB:
            return self.rob == state.rob
        elif comptype == Component.LFB:
            return self.lfb == state.lfb
        elif comptype == Component.HWPREFETCHER:
            return self.hwprefetcher == state.hwprefetcher
        elif comptype == Component.EXESTATUS:
            return self.executionUnitsBusy == state.executionUnitsBusy
        else:
            print('Unknown uarch component type, aborting...\n')
            sys.exit()

    def print_feature(self, comptype):
        if comptype == Component.LQ:  
            return self.lq.__str__()
        elif comptype == Component.SQ:
            return self.sq.__str__()
        elif comptype == Component.ROB:
            return self.rob.__str__()
        elif comptype == Component.LFB:
            return self.lfb.__str__()
        elif comptype == Component.HWPREFETCHER:
            return self.hwprefetcher.__str__()
        elif comptype == Component.EXESTATUS:
            return self.executionUnitsBusy.__str__()
    

    def comp_violators(self, state):
        violators = []
        for component in Component:
           if not self.compare(component, state):
               violators.append(component)
        return violators

    def __str__(self):
        return 'Cycle: ' + \
               str(self.cycle_begin) + '\n' + \
               str(self.rob) + '\n' + \
               str(self.lq) + '\n' + \
               str(self.sq) + '\n' + \
               str(self.lfb) + '\n' + \
               str(self.hwprefetcher) + '\n' + \
               str(self.executionUnitsBusy)

class LoadQueue(CircularQueue):
    def __init__(self):
        self.sn = []
        self.pc = []
        self.address = []
        super(LoadQueue, self).__init__()

    def __eq__(self, lqOther):
        if self.occupancy == lqOther.occupancy:
           if compareContent(self.pc, lqOther.pc):
               return compareContent(self.address, lqOther.address)
        return False        

    def __str__(self):
        return 'LQ: ' + str(self.sn) + '\n' + \
               '[{}]'.format(', '.join(hex(x) for x in self.pc)) + '\n' + \
               '[{}]'.format(', '.join(hex(x) for x in self.address))

    def setmetaData(self):
        super(LoadQueue, self).setmetaData()
        self.sn = self.getValidEntries(self.sn)
        self.pc = self.getValidEntries(self.pc)
        self.address = self.getValidEntries(self.address)

class StoreQueue(CircularQueue):
    def __init__(self):
        self.sn = []
        self.pc = []
        self.address = []
        self.data = []
        super(StoreQueue, self).__init__()

    def __eq__(self, sqOther):
       if self.occupancy == sqOther.occupancy: 
           if compareContent(self.pc, sqOther.pc): #Ordering enforced: if all(x==y for x,y in zip(self.getValidEntries(self.pc), sqOther.getValidEntries(sqOther.pc))):
               return compareContent(self.address, sqOther.address)
                   #return compareContent(self.data, sqOther.data)
       return False

    def __str__(self):
        return 'SQ: ' + str(self.sn) + '\n' + \
               '[{}]'.format(', '.join(hex(x) for x in self.pc)) + '\n' + \
               '[{}]'.format(', '.join(hex(x) for x in self.address))

    def setmetaData(self):
        super(StoreQueue, self).setmetaData()
        self.sn = self.getValidEntries(self.sn)
        self.pc = self.getValidEntries(self.pc)
        self.address = self.getValidEntries(self.address)
        self.data = self.getValidEntries(self.data)

class ROB(CircularQueue):
    def __init__(self):
        self.sn = []
        self.pc = []
        self.inst = []
        super(ROB, self).__init__()

    def __eq__(self, robOther):
        if self.occupancy == robOther.occupancy:
            if compareContent(self.pc, robOther.pc):
                return compareContent(self.inst, robOther.inst)
        return False

    def __str__(self):
        return 'ROB: ' + str(self.sn) + '\n' + \
               '[{}]'.format(', '.join(hex(x) for x in self.pc))

    def setmetaData(self):
        super(ROB, self).setmetaData()
        self.sn = self.getValidEntries(self.sn)
        self.pc = self.getValidEntries(self.pc)
        self.inst = self.getValidEntries(self.inst)

class LineFillBuffer():
    def __init__(self):
        self.data = []

    def __eq__(self, lfbOther):
        return compareContent(self.data, lfbOther.data)

    def __str__(self):
        return 'LFB: ' + '[{}]'.format(', '.join(hex(x) for x in self.data)) 

class RegisterFile():
    def __init__(self, name):
        self.name = name
        self.data = []

    def __eq__(self, regOther):
        return compareContent(self.data, regOther.data)

    def __str__(self):
        return self.name + str(self.data)

class ExecutionUnitsStatus():
    def __init__(self):
        self.reqs = [0 for x in range(len(FunctionalUnits))]

    def __eq__(self, exeStatsOther):
        return self.reqs == exeStatsOther.reqs

    def __str__(self):
        return 'ExecutionStats: ' + str(self.reqs)

class Prefetcher():
    def __init__(self):
        self.data = '' 
        self.address = ''

    def __eq__(self, prefetchOther):
        if self.address == prefetchOther.address:
            return self.data == prefetchOther.data
        return False

    def __str__(self):
        return 'HWPREFETCHER: ' + str(hex(self.address)) + '\n' + str(hex(self.data))
