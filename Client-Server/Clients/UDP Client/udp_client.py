#! /usr/bin/env python
# -*-coding:utf-8 -*-

import socket
import sys

if len(sys.argv) < 3:
    print "Usage:\t./udp_client.py [host] [port]"
    print "Examples:"
    print "\t./udp_client.py www.google.com 80"
    print "\t./udp_client.py 127.0.0.1 5000"

else:
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        print "[*] Sending command to %s:%d" % (host, port)
        s.sendto("AAABBBCCCDDD", (host, port))
        data, addr = s.recvfrom(4096)
        print data

    except Exception, e:
        print str(e)