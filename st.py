#!/usr/local/epics/modules/pythonIoc/pythonIoc

#interpreter on local Xubuntu and sc5.starp
#/home/jaroslav/epics/modules/pythonIoc/pythonIoc
#/usr/local/epics/modules/pythonIoc/pythonIoc

#import basic softioc framework
from softioc import softioc, builder

#import the application
import caenMonit

#run the ioc
builder.LoadDatabase()
softioc.iocInit()

#start the application
caenMonit.run_caenMonit()


#start the ioc shell
softioc.interactive_ioc(globals())


