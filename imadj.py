
from datetime import datetime
from time import sleep

from epics import PV
from softioc.builder import boolOut, stringIn

class imadj:
    #_____________________________________________________________________________
    def __init__(self):
        self.caen_imon_pv = []
        self.caen_imadj_pv = []
        for ibd in xrange(0, 16, 2):
            for ich in xrange(24):
                pvnam = "SY4527:{0:02d}:{1:03d}:".format(ibd, ich)
                self.caen_imon_pv.append( PV(pvnam+"IMon", auto_monitor=False) )
                self.caen_imadj_pv.append( PV(pvnam+"ImAdj", auto_monitor=False) )
        self.run_calib_pv = boolOut("run_calib", on_update=self.run_calib, HIGH=0.1)
        self.calib_stat_pv = stringIn("calib_stat")
        self.msg = "Last done: "

    #_____________________________________________________________________________
    def init(self):
        print "Initializing the current calibration"
        self.calib_stat_pv.set(self.msg+"none")

    #_____________________________________________________________________________
    def run_calib(self, x):
        if x == 0: return
        self.calib_stat_pv.set("Wait calib in progress")

        #first reset adjustments to zero
        for i in self.caen_imadj_pv: i.put(0)

        #wait for measured currents to stabilize
        sleep(4)

        #put the adjustments
        for i in xrange(len(self.caen_imon_pv)):
            ival = "{0:.3f}".format( self.caen_imon_pv[i].get() )
            adj = -1.*float(ival)
            #print ival, adj
            self.caen_imadj_pv[i].put(adj)

        self.calib_stat_pv.set(self.msg + datetime.now().strftime("%Y-%m-%d %H:%M"))









