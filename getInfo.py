from pysnmp.hlapi import*
from tkinter import*
import bulkget, walk, simpleget

#****************************************************************
#              RETRIVE INFO FROM REMOTE HOST
#****************************************************************

def getDefaultInfo(user, ipadr, password, port):
   userCred = UsmUserData(user, password, password)
   remoteHost = UdpTransportTarget((ipadr, port))
   max_calls = 0
   max_rows = 0
   sysDescr = bulkget.request(user, ipadr, password, port, 'SNMPv2-MIB::sysDescr', 
                              max_calls, max_rows)
   sysLoc = bulkget.request(user, ipadr, password, port, 'SNMPv2-MIB::sysLocation',
                              max_calls, max_rows)
   sysUpTime = bulkget.request(user, ipadr, password, port, 'SNMPv2-MIB::sysUpTime',
                              max_calls, max_rows)

   # cpu percentages from UCD-MIB
   cpuUser = bulkget.request(user, ipadr, password, port, 'UCD-SNMP-MIB::ssCpuUser',
                             max_calls, max_rows)
   cpuSys = bulkget.request(user, ipadr, password, port, 'UCD-SNMP-MIB::ssCpuSystem',
                             max_calls, max_rows)
   cpuIdle = bulkget.request(user, ipadr, password, port, 'UCD-SNMP-MIB::ssCpuIdle',
                             max_calls, max_rows)


   return sysDescr, sysLoc, sysUpTime, cpuUser, cpuSys, cpuIdle

def getProcessInfo(user, ipadr, password, port):
   userCred = UsmUserData(user, password, password)
   remoteHost = UdpTransportTarget((ipadr, port))

   #last parameter is for maxRows, '0' means no max.
   #was using this setting for MemoryUsage MIB due to error, but have changed to walk
   procNameGet = bulkget.request(user, ipadr, password, port, 'HOST-RESOURCES-MIB::hrSWRunName', 
                                 0, 0)

   procCPUget = bulkget.request(user, ipadr, password, port, 'HOST-RESOURCES-MIB::hrSWRunPerfCPU',
                                 0, 0)

   # receiving value constraint error when using BulkGet on this MIB after certain number of entries
   # so using walk instead.  Still receiving less entries than PID's.  Not sure why.
   procMemGet = bulkget.request(user, ipadr, password, port, 'HOST-RESOURCES-MIB::hrSWRunPerfMem',
                                 0, 0)

   return procNameGet, procCPUget, procMemGet

def getInterfaceInfo(user, ipadr, password, port):
   userCred = UsmUserData(user, password, password)
   remoteHost = UdpTransportTarget((ipadr, port))

   interDescr = bulkget.request(user, ipadr, password, port, 'IF-MIB::ifDescr', 0, 0)
   interType = bulkget.request(user, ipadr, password, port, 'IF-MIB::ifType', 0, 0)
   interMtu = bulkget.request(user, ipadr, password, port, 'IF-MIB::ifMtu', 0, 0)
   interSpeed = bulkget.request(user, ipadr, password, port, 'IF-MIB::ifSpeed', 0, 0)
   interAdminStat = bulkget.request(user, ipadr, password, port, 'IF-MIB::ifAdminStatus', 0, 0)
   interOperStat = bulkget.request(user, ipadr, password, port, 'IF-MIB::ifOperStatus', 0, 0)

   return interDescr, interType, interMtu, interSpeed, interAdminStat, interOperStat
   
def getTCPinfo(user, ipadr, password, port):
   userCred = UsmUserData(user, password, password)
   remoteHost = UdpTransportTarget((ipadr, port))

   tcpConnState = walk.request(user, ipadr, password, port, 'TCP-MIB::tcpConnState', 0, 0)
  
   return tcpConnState






