
from datetime import datetime
from time import sleep

from epics import PV, caget, caput
from softioc.builder import boolOut, stringIn

class imadj:
    #_____________________________________________________________________________
    def __init__(self):
        print "Initializing the current calibration"
        self.caen_imon_val = []
        self.caen_imadj_val = []
        for ibd in xrange(0, 16, 2):
            for ich in xrange(24):
                pvnam = "SY4527:{0:02d}:{1:03d}:".format(ibd, ich)
                self.caen_imon_val.append( pvnam+"IMon.VAL" )
                self.caen_imadj_val.append( pvnam+"ImAdj.VAL" )
        self.run_calib_pv = boolOut("run_calib", on_update=self.run_calib, HIGH=0.1)
        self.msg = "Last done: "
        self.calib_stat_pv = stringIn("calib_stat", initial_value=self.msg+"none")

    #_____________________________________________________________________________
    def run_calib(self, x):
        if x == 0: return
        self.calib_stat_pv.set("Wait calib in progress")

        #first reset adjustments to zero
        for i in self.caen_imadj_val: caput(i, 0)

        #wait for measured currents to stabilize
        sleep(5)

        #put the adjustments
        for i in xrange(len(self.caen_imon_val)):
            ival = "{0:.3f}".format( caget(self.caen_imon_val[i]) )
            adj = -1.*float(ival)
            #print ival, adj
            caput(self.caen_imadj_val[i], adj)

        #wait for indicated current to update
        sleep(2)

        self.calib_stat_pv.set(self.msg + datetime.now().strftime("%Y-%m-%d %H:%M"))









