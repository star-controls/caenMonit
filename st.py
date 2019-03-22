#!/usr/local/epics/modules/pythonIoc/pythonIoc

#interpreter on local Xubuntu and sc5.starp
#/home/jaroslav/epics/modules/pythonIoc/pythonIoc
#/usr/local/epics/modules/pythonIoc/pythonIoc

#import basic softioc framework
from softioc import softioc, builder

#import the applications
import caenMonit

from imadj import imadj
im = imadj()

#run the ioc
builder.LoadDatabase()
softioc.iocInit()

#start the applications
caenMonit.run_caenMonit()

#start the ioc shell
softioc.interactive_ioc(globals())


