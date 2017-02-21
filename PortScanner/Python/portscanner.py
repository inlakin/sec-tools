#! /usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import subprocess
import sys
from datetime import datetime

print ""
print "=== TCP Scan ==="
print ""

ip = raw_input("IP to scan: ")

t1 = datetime.now()
try:
    for port in range(1,1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not s.connect_ex((ip, port)):
            print "Port " + str(port) + ": open"
        # else:
            # print "Port " + str(port) + ": open"
except KeyboardInterrupt:
    print "[*] Ctrl+C received. Exiting."
except socket.error:
    print "[*] Could not connect to server. Exicting."
except Exception, e:
    print "[*] ", str(e)


t2 = datetime.now()

total = t2 - t1

print ""
print "[*] Scan finished in ", total