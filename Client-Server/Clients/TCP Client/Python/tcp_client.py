#! /usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import sys

CSRF = "\r\n\r\n"

if len(sys.argv) < 3:
    print "Usage:\t./tcp_client [host] [port]"
    print "Examples:"
    print "\t./tcp_client www.google.com 80"
    print "\t./tcp_client 127.0.0.1 5000"
else:

    print ""
    print "=== TCP Client ==="
    print ""

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    try:
        s.connect((host, port))
        print "[*] Connected to %s:%d" % (host, port)
        while (1):
            print "-"*60
            try: 
                command = raw_input("> ")
                s.send(command + CSRF)
                response = s.recv(4096)
                print response
            except Exception, e:
                print str(e)
            except KeyboardInterrupt:
                print "\r[*] Ctrl+C received. Exiting."
                sys.exit()

    except Exception, e:
        print str(e)





