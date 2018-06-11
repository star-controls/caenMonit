
import time
import threading
from datetime import datetime
import sys
_global = sys.modules[__name__]

#full path to created HTML file
#requires 'stylesx.css' to be present there
htmlnam = "/ceph/WWW/SlowControls2018/tpc_caen.html"
#htmlnam = "tpc_caen.html"

#html header and footer
hhead = ['<HTML><HEAD><link rel="stylesheet" type="text/css" href="stylesx.css"> <META HTTP-EQUIV="Refresh" Content="25" url="./"> </HEAD> ',
        '<title>STAR TPC anode high voltage, CAEN SY4527</title> ', '<BODY BGCOLOR=cornsilk>',
        '  <br><table style="padding-top: 20px;">', '<caption style="font-size:160%;">TPC anode high voltage, CAEN SY4527</caption>',
        '  <tr>']
hfoot = ['  </tr>', '  </table>', '</BODY></HTML> ']
#table format, 32 rows and 6 columns  (also 48x4 is possible)
hnrow = 32
hncol = 6
#header for each column
hTabHead = ['    <th class="h0">SEC</th>', '    <th class="h0">CH</th>', '    <th class="h1">Vmon (V)</th>',
            '    <th class="h1">Imon (uA)</th>']
#column separator in header and value lines
hColSepHead = '    <th> </th>'
hColSepVal = '    <td> </td>'
#line separator
hLinSep = '  </tr>\n  <tr>'
#value table items, sechtor and channel number, voltage, current
hValN = '    <td class="d0"; style="font-weight: bold; background-color: #{1}">{0:2d}</td>'
hValV = '    <td class="d0"; style="background-color: #{1}">{0:.1f}</td>'
hValI = '    <td class="d0"; style="background-color: #{1}">{0:.3f}</td>'

#status colors
statcol = {0: '919191', 1: '00d800', 3: 'f9da3c', 5: 'e19015', 512: 'fd0000'}

#sector and channel numbers
numSec = []
numCh = []
valV = []
valI = []
valS = []

#_____________________________________________________________________________
def makeTab():
  #function to create HTML table
  hfile = open(htmlnam, "w")
  #write html header
  for linhead in hhead:
    hfile.write(linhead+"\n")

  #table header
  for icol in range(hncol):
    for hitem in hTabHead:
      hfile.write(hitem+"\n")
    if icol < (hncol-1):
      hfile.write(hColSepHead+"\n")

  #value rows
  for irow in range(hnrow):
    hfile.write(hLinSep)
    for icol in range(hncol):
      #index to arrays of sector and channel numbers, voltages and currents
      idxVal = irow + icol*hnrow
      #test if current status is in statcol dictionary
      if valS[idxVal] not in statcol:
        print idxVal, ": status ", valS[idxVal], " not present in statcol dictionary."
        return
      #put voltage and current values to the html file
      hfile.write(hValN.format(numSec[idxVal], statcol[valS[idxVal]])+"\n")
      hfile.write(hValN.format(numCh[idxVal], statcol[valS[idxVal]])+"\n")
      hfile.write(hValV.format(valV[idxVal], statcol[valS[idxVal]])+"\n")
      hfile.write(hValI.format(valI[idxVal], statcol[valS[idxVal]])+"\n")
      if icol < (hncol-1):
        hfile.write(hColSepVal+"\n")

  #put table footer
  for linfoot in hfoot:
    hfile.write(linfoot+"\n")
  #put last update time, remove ms after decimal point
  hfile.write("<br>\n")
  hfile.write("Last updated: " + str(datetime.now()).split(".")[0] + "\n")
  #close the html file
  hfile.close()

#_____________________________________________________________________________
def webmonTask():
  while True:
    makeTab()
    time.sleep(24)

#_____________________________________________________________________________
def run_webmon(numSec, numCh, valV, valI, valS):
  print "Starting the web page monitor"
  #connect values arrays
  _global.numSec = numSec
  _global.numCh = numCh
  _global.valV = valV
  _global.valI = valI
  _global.valS = valS
  #run monitoring tread
  tid = threading.Thread(target=webmonTask)
  tid.daemon = True
  tid.start()



























