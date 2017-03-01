#! /usr/bin/env python

import socket
import threading
import sys

def handle_client(client):

        while(1):
            request = client.recv(1024)
            print "[*] Received:"
            print request
            client.send("ok")
                
if len(sys.argv) < 3:
    print "Usage:\t./tcp_server [host] [port]"
    print "Example: ./tcp_server 0.0.0.0 999"
else:
    
    print ""
    print "=== TCP SERVER ==="
    print ""

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host, port))

        s.listen(5)

        print "[*] Listening on %s:%d" % (host, port)

        while True:
            client, addr = s.accept()
            print "[*] Connected to %s:%d" % (addr[0], addr[1])

            client = threading.Thread(target=handle_client, args=(client,))
            client.start()

    except Exception, e:
        print str(e)
        print "You might want to try with sudo or use another port"