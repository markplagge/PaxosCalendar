import unittest
import Calendar
import numpy as np
import itertools
import datetime

class Test_CalTests(unittest.TestCase):
    def setUp(self):
        self.startDates = []
        self.endDates = []

        #first names, last names.
        self.fns = ["bob", "john", "ringo", "Paul", "Conan", "Mike"]
        self.lns = ["Mario", "Luigi", "Walker", "LaQuarius", "Edmond", "Aadams"]
        fullNames = [self.fns, self.lns]
        self.fullNames = fullNames
        self.employeeList = []
        for list in itertools.product(*fullNames):
            self.employeeList.append(list)
        # going to use about 50% overlap events for test:
        day,month,year = 10,26,2003
        overlapStartTimes=[100,200,300,400,500]
        overlapEndTimes=[205,305,405,505,505] #edge cases do not overlap!
        nonOverlapStart = [ x for x in range(1000,1800,100)]
        nonOverlapEnd = [ x for x in range(1500,2300,100)]

        for i in range(int(len(self.employeeList) / 2)):
           
            if np.random.beta(.5,.5)  < .5 : #non overlap calendar
                tt = np.random.choice(nonOverlapStart)
                bb = np.random.choice(nonOverlapEnd)
                self.startDates.append(datetime.datetime(year + 1 ,month,day,hour=tt[:2], minute=tt[2:4]))
                self.endDates.append(datetime.datetime(year + 2, month,day,hour=bb[:2],minute=bb[2:4]))
            else:
                z = i % len(overlapStartTimes)
                self.startDates.append(datetime.datetime(year,month,day,overlapStartTimes[z]))
                self.endDates.append(datetime.datetime(year,month,day,overlapEndTimes[z]))

        for i in range(len(self.employeeList)):
 
            self.events.append(CalEvent("TestEvent " + str(i),startDates[i],
                                        endDates[i], participants=[employeeList[i]], 
                                        owner=employeeList[i]))
        return super().setUp()
   
        


    def test_A(self):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
