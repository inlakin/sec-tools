#! /usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import socket
import getopt
import threading
import subprocess
from termcolor import colored

listen      = False
port        = 0
destination = ""
shell       = False

def usage():
    print "=== PyNetcat ==="
    print ""
    print "Some netcat functionalities in python"
    print ""
    print "Usage:"
    print "    [Server]"
    print "    * Bind shell"
    print "         ./pynetcat.py -d 192.168.0.1 -p 999 -l -c" 
    print "    [Client]"
    print "         ./pynetcat.py -d 192.168.0.1 -p 999 "
    print ""
    print "Options:"
    print "         -l, --listen         listen"
    print "         -c, --reverse-shell  initialize a reverse shell"


def client_t(client, addr):

    host = addr[0]
    print "[*] Connection received from %s:%d" % (host, addr[1])
    if shell:
        prompt = "<"+colored(host, 'blue')+":"+colored("#", 'yellow')+"> "

        while True:

            client.send(prompt)

            response = ""

            while "\n" not in response:
                response += client.recv(4096)

            output = run_cmd(response)

            client.send(output)


def run_cmd(cmd):

    cmd =  cmd.rstrip()

    try:
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except:
        response = "[!] PyNetcat : command failed '" + cmd + "'.\n"

    return response        


def client():

    print "[*] Connecting to %s:%d ..." % (destination, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((destination, port))
        print "[*] Connected!"
           
        while True:
            recv_len = 1
            res      = ""
            
            while recv_len:
                data     = s.recv(4096)
                recv_len = len(data)
                res      += data

                if recv_len < 4096:
                    break

            print res,
            
            cmd = raw_input()
            cmd += "\n"
            s.send(cmd)

    except Exception, e:
        print str(e)
        s.close()
        sys.exit(0)

    # r = raw_input("[*] Send information before connecting ?(o/N)")
    
    # print r

    # if r in ("O", "o"):
    #     cmd = raw_input("> ")
    #     cmd += "\n"
    # else:
    #     print "[*] Option not handled. Exiting."
    #     sys.exit(0)


def server():

    global destination

    # If not target is provided, we listen on all interfaces
    if destination == "":
        destination = "0.0.0.0"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((destination, port))
    print ""
    print "[*] Listening on %s:%d" % (destination, port)

    try:

        # Can manage 5 connections at the same time
        s.listen(5)

        while True:
            client, addr = s.accept()

            # Manage client in a new thread
            client_thread = threading.Thread(target=client_t, args=(client,addr))
            client_thread.start()
    except KeyboardInterrupt:
        print "\r[*] Ctrl+C received. Exiting"
        sys.exit(0)


def main():
    
    global listen
    global port 
    global destination
    global shell

    try:
        opt, args = getopt.getopt(sys.argv[1:], "hlp:d:s", ["help", "listen", "port", "destination","shell"])
    except getopt.GetoptError as e:
        print str(e)        
        print ""
        print usage()

    for o, a in opt:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-d", "--destination"):
            destination = a 
        elif o in ("-s", "--shell"):
            shell = True
        else:
            print "[*] Option is not handled"
    
    if port == 0:
        print "[*] You're missing something, John.."
        print ""
        usage()
        sys.exit(0)

    if not listen and len(destination):
        # Pynetcat as a client 
        print "--------------------------"
        print "-                        -"
        print "-   PyNetcat : CLIENT    -"
        print "-                        -"
        print "--------------------------"
        print ""
        client()
    elif listen:
        print "--------------------------"
        print "-                        -"
        print "-   PyNetcat : SERVER    -"
        print "-                        -"
        print "--------------------------"
        print ""
        # Pynetcat as a server
        server()

main()

