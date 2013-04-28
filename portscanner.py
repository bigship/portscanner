# -*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import subprocess
import sys
import os
from datetime import datetime

# port-service mapping.
# locate the sysfile and parse it. use port number as a key
def portServiceMapping(syspath):
    d = {}
    with open(syspath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            content = line.split('/')[0]
            if os.name == 'nt':
                d[content[content.rfind(' ') + 1:]] = content[:content.find(' ')]
            elif os.name == 'posix':
                d[content[content.rfind('\t') + 1:]] = content[:content.find('\t')]
    return d

d = {} 
if os.name == 'nt':
    service_file = "C:\WINDOWS\system32\drivers\etc\services"
    d = portServiceMapping(service_file)
    subprocess.call('cls', shell=True)
elif os.name == 'posix':
    service_file = "/etc/services"
    d = portServiceMapping(service_file)
    subprocess.call('clear', shell=True)

# Ask for input
remoteServer = raw_input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

# print a nice banner with information on which host we are about to scan
print "-" * 60
print "Please wait, scanning remote host", remoteServerIP
print "-" * 60

# Check what time the scan started
t1 = datetime.now()

# Scan well-known ports (reserved ports)
try:
    for port in xrange(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print "Port %d: \t Open. SERVICE NAME=%s" % (port, d.get(str(port), 'unknown'))
        sock.close()
except KeyboardInterrupt:
    print "Press Ctrl-C"
    sys.exit()
except socket.gaierror:
    print "Hostname could not be resolved. Exiting"
    sys.exit()
except socket.error:
    print "Couldn't connect to server"
    sys.exit()

t2 = datetime.now()
total = t2 - t1

print 'Scanning completed in: ', total