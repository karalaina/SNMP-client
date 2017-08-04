
''' gui-2.py: launches gui and displays mib info
    March 19, 2017
'''

from pysnmp.hlapi import*
from tkinter import*
import getInfo
import bulkget, simpleget, walk
import formatData
import time

port = 161
user = ''
remoteIP = 0
password = ''


#**************************************
#         GET INPUT DATA
#**************************************

def show_entry_fields():
   global user, remoteIP, password  
   iptext = StringVar()
   ipLabelLeft = Label(topwin, textvariable=iptext).grid(row=7, column=1, sticky=W)
   ipLabeRight = Label(topwin, textvariable=iptext).grid(row=7, column=7, sticky=W)
   iptext.set("")
   start_time = 0
   end_time   = 0
   remoteIP   = e0.get()
   user       = e1.get()
   password   = e2.get()
   text0.delete("1.0", END)
   print("User: %s\nIP Address: %s\nPassword: %s" % (user, remoteIP, password))
   if remoteIP == "" or user == "" or password == "":
      text0.insert(INSERT, "One of the entry fields is blank, please enter your "
                   "credentials to make a request.\n")
       
   else:
      e0.delete(0,END)
      e1.delete(0,END)
      e2.delete(0,END)
      iptext.set("Agent IP: " + remoteIP)
      defInfo = getInfo.getDefaultInfo(user, remoteIP, password, port)
      formatData.formatDefault(defInfo, text0)   

# basic function to print data for user entered MIB
# ToDo -format
def printBulkSimple(getObj, textWidget, filp):
   try:
      for (errorIndication, errorStatus, errorIndex, varBinds) in getObj:
         if errorIndication:
            print("errorInd: " + errorIndication)
            textarea.insert(INSERT, "errorInd: " + errorIndication)
         elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                errorIndex and sysLoc[int(errorIndex) - 1][0] or '?'))
            textarea.insert(INSERT, '%s at %s' % (errorStatus.prettyPrint(),
                errorIndex and sysLoc[int(errorIndex) - 1][0] or '?'))
         else:
            for element in varBinds:
               element = str(element)
               element = element.split("::")
               if len(element) > 1:
                  textWidget.insert(INSERT, element[1])
                  textWidget.insert(INSERT, "\n")
                  if filp != 0:
                     filp.write("%s\n" % element[1])
                     
   except Exception as e:
      if len(e.args) > 0:
         if e.args[0].find("RequestTimedOut") > 0:
            errorMsg = "Error" + "Request Timed Out, check IP address"
            textWidget.insert(INSERT, errorMsg)
            if filp != 0:
               filp.write("%s\n" % errorMsg)
            print("emsg: " + errorMsg)
         else:
            errorMsg = "Error: " + e.args[0]
            if errorMsg.find("ValueConstraintError") > -1:
               errorMsg = "Value Constraint Error occurred after last printed OID value";
            textWidget.insert(INSERT, errorMsg)
            print("emsg: " + errorMsg)
      else:
         print("error: " + str(e))
         textWidget.insert(INSERT, str(e))
         if filp != 0:
               filp.write("%s\n" % str(e))

#******************************************************************
#                   MENU BUTTON HANDLERS
#******************************************************************

#*********Custom command option handlers (textwidget text2)*********
def getReq():
   filename = e4.get()
   filp = 0
   if len(filename) > 0:
      filp = open(filename, "w+")
   
   mibObject = simpleget.request(user, remoteIP, password, port, e3.get())
   text2.delete("1.0", END)
   if mibObject != "":
      if mibObject[3]:
         if mibObject[3][0]:
            mibStr = str(mibObject[3][0])
            mibStr = mibStr.split("::")
            mibStr = mibStr[1]
            text2.insert(INSERT, mibStr)
            if filp != 0:
               filp.write("%s\n" % mibStr)                       
   else:
      text2.insert(INSERT, "No object available at this OID\n")
   if filp != 0:
      filp.close()

def walkReq():
   max_calls = 0
   max_rows = 0
   filp = 0
   filename = e4.get()
   if len(filename) > 0:
      filp = open(filename, "w+")
      
   mibObjects = walk.request(user, remoteIP, password, port, e3.get(), 
                             max_calls, max_rows)
   text2.delete("1.0", END)
   if mibObjects:
      printBulkSimple(mibObjects, text2, filp)
   if filp != 0:
      filp.close()
     
def bulkGetReq():
   max_calls = 0;
   max_rows = 0;
   filp = 0
   filename = e4.get()
   if len(filename) > 0:
      filp = open(filename, "w+")

   mibObjects = bulkget.request(user, remoteIP, password, port, e3.get(),
                                max_calls, max_rows)
   text2.delete("1.0", END)
   if mibObjects:
      printBulkSimple(mibObjects, text2, filp)
   if filp != 0:
      filp.close()
   
#*********textarea text1 menu button handlers**********
def procGet():
   text1.delete("1.0", END)
   procInfo = getInfo.getProcessInfo(user, remoteIP, password, port)
   text1.config(state=NORMAL)
   text1.delete('1.0', END)
   #******Display table of process info*******
   #*******error handling is done within formatData***
   data = formatData.formatProcessData(procInfo, text1)
   formatData.formatProcessTable(data, text1)   
   
def interGet():
   text1.delete("1.0", END)
   interInfo = getInfo.getInterfaceInfo(user, remoteIP, password, port)
   data = formatData.formatInter(interInfo, text1)
   formatData.formatTable(data, text1)
   
def tcpGet():
   text1.delete("1.0", END)
   tcpInfo = getInfo.getTCPinfo(user, remoteIP, password, port)
   data = formatData.formatTCP(tcpInfo, text1)
   formatData.formatTCPtable(data, text1)


#**********************************************************************
#                            GUI STUFF 
#**********************************************************************

topwin = Tk()
topwin.title("SNMP Client")
topwin.geometry("1350x650")
text0 = Text(topwin, width=50, height=9)
text0.grid(row=0, rowspan=5, column=2, columnspan=3)
text0.config(font = ("Ariel", 10), bd=4, wrap=WORD)

scrollbar = Scrollbar(topwin)
text1 = Text(topwin, width=75, height=20, yscrollcommand=scrollbar.set)
text1.grid(row=8, column=0, columnspan=5)
text1.config(font = ("Courier", 11), bd=4, wrap=WORD)
scrollbar.config(command=text1.yview)
scrollbar.grid(column=5)

scrollbar2 = Scrollbar(topwin)
text2 = Text(topwin, width=60, height=20, yscrollcommand=scrollbar2.set)
text2.grid(row=8, column=7, sticky=W)
text2.config(font = ("Courier", 11), bd=4, wrap=WORD)
scrollbar2.config(command=text2.yview)
scrollbar2.grid(column=10)

Label(topwin, text="IP Address").grid(row=0, sticky=E)
Label(topwin, text="Username").grid(row=1, sticky=E)
Label(topwin, text="Password").grid(row=2, sticky=E)

Label(topwin, text="MIB-OID").grid(row=1, column=6, sticky=E)
Label(topwin, text="Save to File...").grid(row=2, column=6, sticky=E)
Label(topwin, text="SNMP Request Output").grid(row=6, column=7, sticky=W)
Label(topwin, text="Custom Command").grid(row=0, column=7, sticky=W)


defaultMenu = Menubutton(topwin, text="Display...", relief=RAISED, direction=RIGHT)
defaultMenu.menu = Menu(defaultMenu, tearoff=0)
defaultMenu.menu.add_command(label="Process Stats", command=procGet)
defaultMenu.menu.add_command(label="Network Interfaces", command=interGet)
defaultMenu.menu.add_command(label="TCP Connections", command=tcpGet)
defaultMenu["menu"] = defaultMenu.menu
defaultMenu.grid(row=7, column=0, sticky=W)

#***********Create Menu Button with custom command options
commandmenu = Menubutton(topwin, text="Select SNMP Command...", relief=RAISED, direction=RIGHT)
commandmenu.menu = Menu(commandmenu, tearoff=0)
commandmenu.menu.add_command(label="get", command=getReq)
commandmenu.menu.add_command(label="walk", command=walkReq)
commandmenu.menu.add_command(label="bulkget", command=bulkGetReq)
commandmenu["menu"] = commandmenu.menu
commandmenu.grid(row=4, column=7, sticky=W)

e0 = Entry(topwin)
e1 = Entry(topwin)
e2 = Entry(topwin, show="*")
e3 = Entry(topwin, width=30) #custom oid entry field
e4 = Entry(topwin, width=30) #file save entry

e0.grid(row=0, column=1, sticky=W)
e1.grid(row=1, column=1, sticky=W)
e2.grid(row=2, column=1, sticky=W)
e3.grid(row=1, column=7, sticky=W)
e4.grid(row=2, column=7, sticky=W) #file save entry
Button(topwin, text='Submit', command=show_entry_fields).grid(row=3, column=1, sticky=W)

topwin.mainloop()

