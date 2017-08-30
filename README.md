A remote system monitor utitilizing the Simple Network Management Protocol (SNMP) built with the PySNMP python library. 

Authors: Kara Campbell and Tom Buckley

The Simple Network Management Protocol (SNMP), was designed for remote system monitoring and configuration over an Internet Protocol (IP) network.  It provides a simple interface for one system, typically called the manager, to access information about the devices on it’s network, the agents.   

One of the main advantages to SNMP is that it is implementation independent and works across a wide variety of hardware.   Information is requested using Object Identifiers (OID’s) contained in a Management Information Base (MIB).  The MIB is a hierarchical structure consisting of a collection of objects.  Each object describes a type of information, such as the uptime of a server, or a table of open TCP connections.  Some OID’s are read-only, while others can be modified.

SNMP commands can be executed on a command line.  For the development of larger and more complex applications using SNMP, a python library (PySNMP) was developed by Ilya Etingof.  Our application was designed on top of these protocols and libraries.




