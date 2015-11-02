__author__ = 'plaggm'
import datetime
from collections import namedtuple
import unittest
import pickle
import random
import jsonpickle
import json
import numpy as np

busyT = namedtuple('busyT', ['start', 'end'])
emp = namedtuple('emp', ['firstName', 'lastName'])

##Helper Functions - DateTIme to/from JSON
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object
## CalEvent Factory - Goes from JSON to a brand new JSON object

def genCalEvt(text):
    cc = CalEvent()
    cc.fromJSON(text)
    return cc


def DateTimeDecoder(timeList):
    timeList = map(lambda i: int(i), timeList)
    return datetime.datetime(*timeList)

###
#########FACTORY FOR FILE/IO #####
# Factory Pattern for init from JSON or File:
# Note: Actual class may not include any factory pattern.

class CalGenerator(object):
    def __init__(self, source="FILE", type="JSON", fileName="", stream="", uuid=""):
        self.source = source
        self.fileName = fileName
        self.stream = stream
        self.type = type
        self.uuid = uuid
        if uuid is not "":
            tmpc = Calendar(uuid)
            if type is "JSON":
                self.fileName = tmpc.hrfn
            else:
                self.fileName = tmpc.mrfn

    def getGen(self):
        if self.type is "JSON":
            return self.initFromJSON

    def initFromJSON(self, jsSrc):
        if self.source is "FILE":
            self.ldd = jsonpickle.loads(jsSrc.read())
        if self.source is "NETWORK":
            self.ldd = jsonpickle.loads(jsSrc)
        self.newCal = Calendar(self.ldd["myUID"])
        evtList = list(map(lambda cvt: genCalEvt(cvt), self.ldd["caltxts"]))
        for evt in evtList:
            self.newCal.addEntry(evt)
        return self.newCal

    def initFromBin(self):
        self.newCal = Calendar("EMPTY")
        self.newCal.fileName = self.fileName
        self.newCal.loadCal()
        return self.newCal

    def initCalFromFile(self):
        if self.type is "JSON":
            with open(self.fileName, 'r') as jsfile:
                self.initFromJSON(jsfile)
        else:
            if self.source is "FILE":
                self.initFromBin()
        return self.newCal

    def createCal(source="FILE", type="JSON", fileName="", stream="", uuid=""):
        gen = CalGenerator(source, type, fileName, stream, uuid)
        return gen.initCalFromFile()


class wuLog:
    def _init__(self):
        self.log = []

    def addLogEntry(self, clock, evtType, calvt):
        pass

class wuTT:
    def __init__(self, nps=3, myID=0):
        self.matrix = np.zeros(nps)
#########

class CalEvent(object):

    def __init__(self, eventName = "not a real eventName", startTS=datetime.datetime.now(), 
                 endTS=datetime.datetime.now(), uRank=0, participants=[], owner="Self",
                 insertTime=datetime.datetime.now(), lamportClock=[0,0]):
        self.eventName = eventName
        self.startTS = startTS
        self.endTS = endTS

        self.urank = 0
        self.participants = participants
        self.owner = owner
        self.insertTime = insertTime
        self.lamportClock = lamportClock
   

    def __str__(self):
        elements = {}
        data = ''
        x = vars(self)
        y = 0
        for key, value in x.items():
            y += 1
            if not isinstance(value,datetime.datetime):
                data = data + '{}: {}\n'.format(key,value)
        assert(isinstance(self.startTS,datetime.datetime))
        d = datetime.datetime.now()
        data += "From {} to {}".format(self.startTS.isoformat(),self.endTS.isoformat())
        return data

    def __eq__(self, other):
        #Currently checks to see if startdate, enddate and participants are the same:
        if(isinstance(other,CalEvent)):
            
            ptMatch = sorted(self.participants) == sorted(other.participants)
            timeMatch = (self.startTS == other.startTS) and (self.endTS == other.startTS)
            
            return ptMatch and timeMatch
        return False
             
                                
    @property
    def uName(self):
        return self.owner
    @property
    def uniqueID(self):
        return object.__hash__(self)
    @property
    def eventRange(self):
        return busyT(start=self.startTS, end=self.endTS)
    def compareAge(self, other):
        """

        :param other: the other cal entry
        :return: was this entry added before the other entry?(Is this entry newer?)
        """
        return self.insertTime - other.insertTime < datetime.timedelta(seconds=1)
    
    def calculateOverlap(self, othCal):
        assert isinstance(othCal, CalEvent)
        return self.eventRange.start < othCal.eventRange.end and othCal.eventRange.start < self.eventRange.end

        # mStart = max(self.eventRange.start, othCal.eventRange.start)
        #
        # mEnd = max(self.eventRange.end, othCal.eventRange.end)
        # return (mEnd - mStart)

    def willEventConflict(self, othCal):
        assert isinstance(othCal, CalEvent)
        overlap = self.calculateOverlap(othCal)
        #assert isinstance(overlap, datetime.timedelta)

        collab = False

        # for part in othCal.participants:
        #     collab = collab or int(self.uName) == int(part)
        cbs = list(filter(lambda part: part in self.participants, othCal.participants))

        for participant in self.participants:
            for oPart in othCal.participants:
                collab = collab or participant == oPart


        return (overlap and collab)


    def shouldAcquiesce(self, othCal):
        # compare and contrast the other item. Need more complex system
        assert isinstance(othCal, CalEvent)
        return (self != othCal or
                (self.willEventConflict(othCal)
                 and (self.compareRank(othCal) or othCal.compareAge(self))
                 )
                )
    def toJSON(self):

        output = ""
        elements = self.__dict__
        elements["startTS"] = self.startTS
        elements["endTS"] = self.endTS
        elements["insertTime"] = self.insertTime
        return json.dumps(elements, cls=DateTimeEncoder, sort_keys=True, indent=2, separators=(',',': '))

    def fromJSON(self, text):
        result = jsonpickle.loads(text)

        result["startTS"] = DateTimeDecoder(result["startTS"])
        result["endTS"] = DateTimeDecoder(result["endTS"])
        result["insertTime"] = DateTimeDecoder(result["insertTime"])
        # bt1 = DateTimeDecoder(result["eventRange"][0])
        # bt2 = DateTimeDecoder(result["eventRange"][1])
        # result["eventRange"] = busyT(start=bt1, end=bt2)
        self.__dict__ = result
        return result


### FULL CAL EVENT:
class Calendar(object):
    myUID = 0
    fileName = str(myUID) + "_caldata.csv"

    cal = []
    caltxts = []

    def __init__(self, username=0):
        if (username != ""):
            self.myUID = username
            self.fileName = str(self.myUID) + "_caldata"
            self.hrfn = "hum_" + str(self.myUID) + "_caldata.json"
            self.mrfn = "dat_" + str(self.myUID) + "_caldata.dat"
            self.cal = []
            self.caltxts = []

    def __eq__(self, other):

        itms = True
        for evt in self.cal:
            matchedone = False

            for ote in other.cal:
                matchedone = matchedone or (evt == ote)

            itms = itms and matchedone
        return (isinstance(other, Calendar)
                and self.myUID == other.myUID
                and self.fileName == other.fileName
                and itms
                )

    def __str__(self, **kwargs):
        strout = "Calendar for %s:\n"+ str(self.myUID)
        strout += map(lambda evt: str(evt) + "\n", self.cal)
        return strout


    def saveCal(self):
        # pickled = []
        # for row in self.cal:
        #    pickled.append(jsonpickle.encode(row))
        # file = open(self.fileName, 'w')
        # for row in pickled:
        #    file.write(row)
        # file.close()
        self.cal.sort()
        with open(self.mrfn, 'wb') as f:
            pickle.dump(self.cal, f, pickle.HIGHEST_PROTOCOL)

        with open(self.hrfn, 'w') as f:
            self.caltxts = list(self.cal)
            btext = map(lambda i: i.toJSON(), self.caltxts)
            self.caltxts = list(btext)
            bigDict = dict(self.__dict__)
            del (bigDict["cal"])

            js1 = json.dumps(bigDict, indent=4, sort_keys=True)
            f.writelines(js1)

