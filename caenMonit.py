
import time
import threading

import epics
from softioc import builder
from webmon import run_webmon

#local PVs
builder.SetDeviceName("tpc_caen_monit")
#trip indicator
trip_pv = builder.boolIn("is_trip", ZNAM=0, ONAM=1)
#anode sum current, inner and outer
sum_curr_in_pv = builder.aIn("sum_curr_in")
sum_curr_out_pv = builder.aIn("sum_curr_out")

#status of tripped channel
tripstat = 512

#voltage and current values, status value
npv=192
valV = [0. for i in range(npv)]
valI = [0. for i in range(npv)]
valS = [0 for i in range(npv)]

#sector and channel numbers
numSec = [None]*npv
numCh = [None]*npv
#dictionary from PV board and chan to array index
pdict = {}
#inner/outer channels, 0 = inner, 1 = outer
inout = [0 for i in range(npv)]


#_____________________________________________________________________________
def onValueChange(pvname=None, value=None, **kws):
  #function called on PV value change
  ppart = pvname.split(":")
  ibd = int(ppart[1])
  ichan = int(ppart[2])
  ival = pdict[(ibd, ichan)]
  ptype = ppart[3]
  if ptype == "VMon":
    valV[ival] = value
  elif ptype == "IMon":
    valI[ival] = value
  elif ptype == "Status":
    valS[ival] = value
    #check for trip
    if value == tripstat:
      trip_pv.set(1)

#_____________________________________________________________________________
def init_caen_pvs():
  #table format
  id_ilist = 0
  id_sec = 1
  id_ch = 2
  id_bd = 3
  id_chan = 4
  #PV lists
  plistV = []
  plistI = []
  plistS = []
  #initialize PV lists and dictionary from lookup table
  iline=0
  for line in open("caen_lookup_table_v1.txt", "r"):
    lintab = [int(item) for item in line.split(" ")]
    numSec[iline] = int(lintab[id_sec])
    numCh[iline] = int(lintab[id_ch])
    #dictionary from PV board and chan to array index
    pdict[(lintab[id_bd], lintab[id_chan])] = iline
    #inner/outer channels
    if numCh[iline] <= 4:
      inout[iline] = 0
    else:
      inout[iline] = 1
    #PV names
    pnamV = "SY4527:{0:02d}:{1:03d}:VMon".format(lintab[id_bd], lintab[id_chan])
    pnamI = "SY4527:{0:02d}:{1:03d}:IMon".format(lintab[id_bd], lintab[id_chan])
    pnamS = "SY4527:{0:02d}:{1:03d}:Status".format(lintab[id_bd], lintab[id_chan])
    pvV = epics.PV(pnamV, callback=onValueChange)
    pvI = epics.PV(pnamI, callback=onValueChange)
    pvS = epics.PV(pnamS, callback=onValueChange)
    plistV.append(pvV)
    plistI.append(pvI)
    plistS.append(pvS)
    iline += 1

#_____________________________________________________________________________
def tripmon():
  #trip monitoring function
  #PV for trip is also set in onValueChange, need to clear here
  ntrip = 0
  for i in range(len(valS)):
    if valS[i] == tripstat: ntrip += 1
  if ntrip == 0:
    trip_pv.set(0)
  else:
    trip_pv.set(1)

#_____________________________________________________________________________
def tripmonTask():
  while True:
    time.sleep(3)
    tripmon()

#_____________________________________________________________________________
def run_tripmon():
  print "Starting the trip monitor"
  #run trip monitoring tread
  tid = threading.Thread(target=tripmonTask)
  tid.daemon = True
  tid.start()

#_____________________________________________________________________________
def currmon():
  #sum current monitoring
  csum_in = 0.
  csum_out = 0.
  for i in range(len(valI)):
    if inout[i] == 0:
      csum_in += valI[i]
    else:
      csum_out += valI[i]
  #put sums to PVs
  sum_curr_in_pv.set(csum_in)
  sum_curr_out_pv.set(csum_out)

#_____________________________________________________________________________
def currmonTask():
  while True:
    time.sleep(4)
    currmon()

#_____________________________________________________________________________
def run_currmon():
  print "Starting sum current monitor"
  #run sum current tread
  tid = threading.Thread(target=currmonTask)
  tid.daemon = True
  tid.start()

#_____________________________________________________________________________
def run_caenMonit():
  #connect CAEN PVs
  init_caen_pvs()
  #run monitoring tasks
  run_webmon(numSec, numCh, valV, valI, valS)
  trip_pv.set(0)
  run_tripmon()
  run_currmon()





















