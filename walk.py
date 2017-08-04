from pysnmp.hlapi import*

# snmpwalk module
# params:  ipadr: remote IP, pw: password and encryption key,
#          oid: User requested OID
# returns: nextCmd(...), an iterable object
#          containing MIB variables.
#

def request(user, ipadr, pw, port, oid, m_Calls, m_Rows):

   remoteIP = ipadr
   password = pw
   walk     = ""
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
   
   if len(mibName) and len(oidName) > 0:
      userCred = UsmUserData(user, password , password)
      remoteHost = UdpTransportTarget((remoteIP, port), timeout=1, retries=1)

      walk = nextCmd(SnmpEngine(), userCred, remoteHost, ContextData(),
                      ObjectType(ObjectIdentity(mibName, oidName)),
                      lexicographicMode = False, maxCalls=m_Calls, maxRows=m_Rows)
                      
   elif len(oidNumeric) > 0:
      userCred = UsmUserData(user, password , password)
      remoteHost = UdpTransportTarget((remoteIP, port), timeout=1, retries=1)

      walk = nextCmd(SnmpEngine(), userCred, remoteHost, ContextData(),
                      ObjectType(ObjectIdentity(oidNumeric)),
                      lexicographicMode = False, maxCalls=m_Calls, maxRows=m_Rows)
                      
   return walk

