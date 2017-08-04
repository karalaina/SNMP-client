from pysnmp.hlapi import*
import pysnmp.error

# snmpbulkget module
# params:  ipadr: remote IP, pw: password and encryption key,
#          Oid: User requested OID
#          m_Rows: option for maxRows, 0 gives no limit,
#          m_Rows > 0 puts limit
# returns: bulkCmd(...), an iterable object
#          containing MIB variables, or an error message, 
#          if unable to complete request

def request(user, ipadr, pw, port, oid, m_Calls, m_Rows):

   remoteIP = ipadr
   password = pw
   bulkGet  = ""
   mibName  = ""
   oidName  = ""
   oidNumeric = ""
   
   if oid.find("::") > -1:
      oid = oid.split("::")
      mibName = oid[0]
      oidName = oid[1]
      print("user entered mibName: ", mibName)
      print("user entered oidName: ", oidName)

   #suppose use entered numeric format, if no "::"
   #code iterating over command generator returned by this
   #function will catch any errors
   else:
      oidNumeric = oid
   print(remoteIP, password, oid)
  
   #OID descriptive
   if len(mibName) > 0 and len(oidName) > 0:
      userCred = UsmUserData(user, password , password)
      remoteHost = UdpTransportTarget((remoteIP, port), timeout=1, retries=1)
         
      bulkGet = bulkCmd(SnmpEngine(), userCred, remoteHost, ContextData(), 0, 5,
                      ObjectType(ObjectIdentity(mibName, oidName)),
                      lexicographicMode = False, maxCalls=m_Calls, maxRows=m_Rows)
   #OID numeric
   elif len(oidNumeric) > 0:
      userCred = UsmUserData(user, password , password)
      remoteHost = UdpTransportTarget((remoteIP, port), timeout=1, retries=1)
         
      bulkGet = bulkCmd(SnmpEngine(), userCred, remoteHost, ContextData(), 0, 5,
                      ObjectType(ObjectIdentity(oidNumeric)),
                      lexicographicMode = False, maxCalls=m_Calls, maxRows=m_Rows)
            
   return bulkGet
      
   

