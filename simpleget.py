from pysnmp.hlapi import*

# snmpget module
# params:  ipadr: remote IP, pw: password and key
#          oid: user requested OID
# returns: mibVars, MIB variable
#          data is contained in varBinds[3]

def request(user, ipadr, pw, port, oid):

   remoteIP = ipadr
   password = pw
   bulkGet  = ""
   mibVars  = ""
   mibName  = ""
   oidName  = ""
   oidNameIndex = ""
   oidIndex = ""
   oidNumeric = ""
   
   print(oid)
   if oid.find("::") > -1:
      oid = oid.split("::")
      mibName = oid[0]
      oidNameIndex = oid[1]
      oidNameIndex = oidNameIndex.split(".")
      oidName = oidNameIndex[0]
      oidIndex = ""
      if len(oidNameIndex) > 1:
         oidIndex = oidNameIndex[1]
         print("user entered oidInst: ", oidIndex)
         print("user entered mibName: ", mibName)
         print("user entered oidName: ", oidName)
   
   else:
      oidNumeric = oid
   
   print(remoteIP, password, oid)
   

   if len(mibName) > 0 and len(oidName) > 0 and len(oidIndex) > 0:
      userCred = UsmUserData(user, password , password)
      remoteHost = UdpTransportTarget((remoteIP, port), timeout=1, retries=1)

      get = getCmd(SnmpEngine(), userCred, remoteHost, ContextData(),
                      ObjectType(ObjectIdentity(mibName, oidName, oidIndex)))

      mibVars = next(get)
      
   elif len(oidNumeric) > 0:
      userCred = UsmUserData(user, password , password)
      remoteHost = UdpTransportTarget((remoteIP, port), timeout=1, retries=1)

      get = getCmd(SnmpEngine(), userCred, remoteHost, ContextData(),
                      ObjectType(ObjectIdentity(oidNumeric)))

      mibVars = next(get)
  
      
   return mibVars

  
