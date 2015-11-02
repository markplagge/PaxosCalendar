import unittest
import Calendar
import numpy as np
import itertools
import datetime
def genUsersOfEvent(nameList, num):
     rdmr = np.random.permutation(nameList)
     test = [x[0] + " " + x[1] for x in rdmr[0:num]]
     #parts = rdmr[0:num]
     #parts = list(map(lambda name: name[0] + " " + name[1], parts))
     own = test[0]    
     
     return test,own


class Test_CalTests(unittest.TestCase):
    def setUp(self):
        self.startDates = []
        self.endDates = []

        #first names, last names.
        self.fns = ["bob", "john", "ringo", "Paul", "Conan", "Mike"]
        self.lns = ["Mario", "Luigi", "Walker", "LaQuarius", "Edmond", "Aadams"]
        self.fullNames = [self.fns,self.lns]
        #create four events for checking
        self.events=[]
        year,month,day = 2001,1,1
        startTimes = ['0800','0900','1600','2000']
        endTimes = ['0930', '1550','2001','2100']
        self.overlaps = [(0,1),(2,3)]
        self.employeeList = []
        for list in itertools.product(*self.fullNames):
            self.employeeList.append(list)

        for i in range(0,3):
            pts,own = genUsersOfEvent(self.employeeList,3)
            startH = int(startTimes[i][:2])
            startM = int(startTimes[i][2:4])
            endH = int(endTimes[i][:2])
            endM = int(endTimes[i][2:4])

            self.events.append(Calendar.CalEvent('Test Event ' + str(i), startTS = datetime.datetime(year,month,day,startH,startM),
                                                 endTS = datetime.datetime(year,month,day,endH,endM),participants=pts,owner=own))

        return super().setUp()
   
        

    def testWillEventConflict(self):
        for pair in self.overlaps:
            coll = self.events[pair[0]].willEventConflict(self.events[pair[0]])
            assert(coll)

    def testEqualityOfEvents(self):
        #Events are equal if:
        #Participants are the same, start and end times are the same, name is the same.
        startTime = datetime.datetime.now()
        endTime = datetime.datetime.now()
        parts,own = genUsersOfEvent(self.employeeList,5)
        newEvt1 = Calendar.CalEvent('Test Equality Event',startTS = startTime, endTS = endTime,participants = parts, owner=own)
        newEvt2 = Calendar.CalEvent('Test Equality Event',startTS = startTime, endTS = endTime,participants = parts, owner=own)
        assert(newEvt1 == newEvt2)

    def testStr(self):
        print(self.events[0])
        pass

if __name__ == '__main__':
    unittest.main()
