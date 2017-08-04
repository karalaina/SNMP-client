from tkinter import*
import pysnmp.error

# printDefaultMibs: used for printing default data into small
#                   textarea: text0
# params: mibGenerator: command generator returned by bulkCmd(),
#         label: name of mib, 
#         units: units of value, eg "%", if necessary.
#         textarea: text widget in window
def printDefaultMibs(mibGenerator, label, units, textarea):

   for (errorIndication, errorStatus, errorIndex, varBinds) in mibGenerator:
      if errorIndication:
         print("errorInd: ", errorIndication)
         textarea.insert(INSERT, "errorInd: " + errorIndication)
      elif errorStatus:
         print('%s at %s' % (errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
         textarea.insert(INSERT, '%s at %s' % (errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
      else:
         for i in varBinds:
            mibstr = str(i)
            mibstr = mibstr.split("= ")
            if len(mibstr) > 1:
               textarea.insert(INSERT, "%s: " % label)
               textarea.insert(INSERT, mibstr[1])
               textarea.insert(INSERT, "%s\n" % units)

#****Array helper functions*************
# append proc index(which is PID) to pidArr
# and name to nameArr
def appendProcNameAndPid(mibstr, nameArr, pidArr):
   mibstr = mibstr.split("=")
   if len(mibstr) > 1:
      pidArr.append(mibstr[0])
      nameArr.append(mibstr[1])
      
#append mib value only to array: arr
#no index required
def appendMibValueOnly(mibstr, arr):
   mibstr = mibstr.split("=")
   if len(mibstr) > 1:
      arr.append(mibstr[1])
      
# append tcp data. One string from OID 'tcpConnState'
# is parsed for multiple values
def appendTCPdata(mibstr, arr):
   mibstr = mibstr.split(".")
   #local addresses at arr[0]
   arr[0].append(mibstr[0] + "." + mibstr[1] + "."
                 + mibstr[2] + "." + mibstr[3])
   #local ports at arr[1]
   arr[1].append(mibstr[4])
   #remote addresses at arr[2]
   arr[2].append(mibstr[5] + "." + mibstr[6] + "."
                 + mibstr[7] + "." + mibstr[8])
   #remote ports at arr[3], and contained in mibstr[9]
   #along with actual connection state value
   mibstr[9] = mibstr[9].split("=")
   arr[3].append(mibstr[9][0])
   #connection state at arr[4]
   arr[4].append(mibstr[9][1])
   
      
# addMibValuesToArr():  add data to an array(s) for future processing
# params: mibGenerator: command generator returned by bulkCmd(),
#         mibValArr:    array for storing mib values
#         mibIndexArr:  array for storing index (used for PID'S)
#         tcpFlag:      (integer): when greater than 0, call
#                       appendTCPdata() to deal with different tcp data
#                       NOT A GREAT solution, is confusing and adds complexity
#                       but minimizes code repetition for now
#         stripIndex:   index of full MIB string to start from(used for PID and TCP strings)
#         label:        name, units, 
#         textarea:     text widget in window

def addMibValuesToArr(mibGenerator, mibValArr, mibIndexArr, tcpFlag, stripIndex, textarea):
   for (errorIndication, errorStatus, errorIndex, varBinds) in mibGenerator:
      if errorIndication:
         print("errorInd: " + errorIndication)
         textarea.insert(INSERT, "errorInd: " + errorIndication)
      elif errorStatus:
         print('%s at %s' % (errorStatus.prettyPrint(), 
                  errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
         textarea.insert(INSERT, '%s at %s' % (errorStatus.prettyPrint(), 
                  errorIndex and varBinds[int(errorIndex) - 1][0] or '?')) 
      else:
         for i in varBinds:
            mibstr = str(i)        
            if stripIndex > 0:
               #add data to tcp info array
               if tcpFlag > 0:
                  mibstr = mibstr[stripIndex:]
                  appendTCPdata(mibstr, mibValArr)
               #add data to process pid and name arrays
               else: 
                  mibstr = mibstr[stripIndex:]
                  appendProcNameAndPid(mibstr, mibValArr, mibIndexArr)
            #add data to interface array, only value needed
            else:
               appendMibValueOnly(mibstr, mibValArr)

#****Create interface arrays, add mib data to arrays*****
def formatInter(interMibs, text1):
   names = []
   types = []
   mtus = []
   speed  = []
   admin = []
   oper  = []

   try:
      addMibValuesToArr(interMibs[0], names, 0, 0, 0, text1)
      addMibValuesToArr(interMibs[1], types, 0, 0, 0, text1)
      addMibValuesToArr(interMibs[2], mtus, 0, 0, 0, text1)
      addMibValuesToArr(interMibs[3], speed, 0, 0, 0, text1)
      addMibValuesToArr(interMibs[4], admin, 0, 0, 0, text1)
      addMibValuesToArr(interMibs[5], oper, 0, 0, 0, text1)

   except Exception as e:
      if len(e.args) > 0:
         if e.args[0].find("RequestTimedOut") > 0:
            errorMsg = "Error" + "Request Timed Out, check IP address"
            text1.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
         else:
            errorMsg = "Error: " + e.args[0]
            if errorMsg.find("ValueConstraintError") > -1:
               errorMsg = "Value Constraint Error with value with this OID"
            #text1.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
      else:
         print("error: " + str(e))
         text1.insert(INSERT, str(e))

   return names, types, mtus, speed, admin, oper


#********Format interface table****
def formatTable(data, text1):
   names = data[0]
   types = data[1]
   mtus  = data[2]
   speed = data[3]
   admin = data[4]
   oper  = data[5]

   numInter = len(data[0])

   count = 0
   while (count < numInter):
      text1.insert(INSERT, "Description: %s\n" % names[count])
      text1.insert(INSERT, "Type: %s\n" % types[count])
      text1.insert(INSERT, "Maximum transmission unit (MTU): %s\n" % mtus[count])
      text1.insert(INSERT, "Speed (bits/s): %s\n" % speed[count])
      text1.insert(INSERT, "Admin Status: %s\n" % admin[count])
      text1.insert(INSERT, "Operational Status: %s\n" % oper[count])
      text1.insert(INSERT, "\n")
      count += 1


#****Format Process Data, create arrays for mib data****
def formatProcessData(procMibs, text1):

   pids      = []
   procNames = []
   cpuTime   = []
   memUsage  = []
   
   try:
      addMibValuesToArr(procMibs[0], procNames, pids, 0, 32, text1)
      addMibValuesToArr(procMibs[1], cpuTime, 0, 0, 0, text1)
      addMibValuesToArr(procMibs[2], memUsage, 0, 0, 0, text1)
   
   except Exception as e:
      if len(e.args) > 0:
         if e.args[0].find("RequestTimedOut") > 0:
            errorMsg = "Error" + "Request Timed Out, check IP address"
            text1.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
         else:
            errorMsg = "Error: " + e.args[0]
            if errorMsg.find("ValueConstraintError") > -1:
               errorMsg = "Value Constraint Error occured after last printed OID value"
            #text1.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
      else:
         print("error: " + str(e))

   return pids, procNames, cpuTime, memUsage
   
   
#****Format process table****
def formatProcessTable(data, text1):

   pids      = data[0]
   procNames = data[1]
   cpuTime   = data[2]
   memUsage  = data[3]

   countPids = 0
   countCPUtime = 0
   countMem = 0
   lineNum = 5;  #starting line in text1 after headings
   numPids = len(pids)
   numCpuTime  = len(cpuTime)
   numMem      = len(memUsage)
 
   text1.insert(INSERT, "PID      NAME              Total CPU Time          MEM (kB)\n")
   text1.insert(INSERT, "                        consumed by process\n")
   text1.insert(INSERT, "                           (centiseconds)\n")
   text1.insert(INSERT, "-----------------------------------------------------------\n")

   while (countPids < numPids):
      text1.insert(INSERT, pids[countPids])
      #insert spaces
      for k in range(1, 8 - len(pids[countPids])):
         text1.insert(INSERT, " ")
      text1.insert(INSERT, procNames[countPids])
      #insert spaces
      for m in range(1, 27 - len(procNames[countPids])):
         text1.insert(INSERT, " ")
      text1.insert(INSERT, "\n") # needs to be newline to insert more data at "end" of same row.
      countPids += 1

   while (countCPUtime < numCpuTime):
      text1.insert("%d.end" % lineNum, cpuTime[countCPUtime])
      for x in range(1, 18-len(cpuTime[countCPUtime])):
         text1.insert("%d.end" % lineNum, " ")
      lineNum+=1
      countCPUtime+=1

   #restart lineNum for memUsage data
   lineNum = 5
   while (countMem < numMem):
      text1.insert("%d.end" % lineNum, memUsage[countMem])
      lineNum+=1
      countMem+=1

#****add tcpConnState mib data to arrays****
def formatTCP(tcpMibs, text1):
   tcpRowData = []
   localAdr   = []
   localPort  = []
   remoteAdr  = []
   remotePort = []
   states     = []
 
   tcpRowData.append(localAdr)
   tcpRowData.append(localPort)
   tcpRowData.append(remoteAdr)
   tcpRowData.append(remotePort)
   tcpRowData.append(states)

   try:
      addMibValuesToArr(tcpMibs, tcpRowData, 0, 1, 22, text1)
   except Exception as e:
      if len(e.args) > 0:
         if e.args[0].find("RequestTimedOut") > 0:
            errorMsg = "Error" + "Request Timed Out, check IP address"
            text1.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
         else:
            errorMsg = "Error: " + e.args[0]
            if errorMsg.find("ValueConstraintError") > -1:
               errorMsg = "Value Constraint Error occured after last printed OID value"
            #text1.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
      else:
         print("error: " + str(e))
 
   return tcpRowData

def formatTCPtable(data, text1):

   text1.insert(INSERT, "Local Address  Local Port  Remote Address  Remote Port  State \n")
   text1.insert(INSERT, "--------------------------------------------------------------\n")

   numRows = len(data[0])
   numCols = len(data)
   i = 0 #index to access data in given row of data[][]
   col = 0
   while (i < numRows):
      for entry in data:
         text1.insert(INSERT, entry[i])
         if col == 0 or col == 2:
            for k in range(1, 18 - len(entry[i])):
               text1.insert(INSERT, " ")
         elif col == 1 or col == 3:
            for k in range(1, 10 - len(entry[i])):
               text1.insert(INSERT, " ")
         col+=1
      text1.insert(INSERT, "\n")
      col = 0
      i+=1


#*****display some default data in textwidget: text0****
def formatDefault(defMibs, text0):
   try:
      
      printDefaultMibs(defMibs[0], "System Description", "", text0)         
      printDefaultMibs(defMibs[1], "Location", "", text0)               
      printDefaultMibs(defMibs[2], "System Uptime", " s", text0)
      text0.insert(INSERT, "---Overall CPU, Mem, Storage Usage---\n")
      printDefaultMibs(defMibs[3], "User CPU Time", "%", text0)          
      printDefaultMibs(defMibs[4], "System CPU Time", "%", text0)
      printDefaultMibs(defMibs[5], "Idle CPU Time", "%", text0)
          
   except Exception as e:
      if len(e.args) > 0:
         if e.args[0].find("RequestTimedOut") > 0:
            errorMsg = "Error" + "Request Timed Out, check IP address"
            text0.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
         else:
            errorMsg = "Error: " + e.args[0]
            if errorMsg.find("ValueConstraintError") > -1:
               errorMsg = "Value Constraint Error occured after last printed OID value"
                           
            text0.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
      else:
         print("error: " + str(e))
         if str(e).find("WrongValueError()") > 0:
            text0.insert(INSERT, "Incorrect username or password\n")



    
