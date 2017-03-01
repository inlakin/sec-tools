#! /usr/bin/env python
# -*- coding=utf-8 -*-


import sys
import getopt
import re
import random
from scapy.all import *

from datetime import datetime

destination = ""
s_port      = 0
e_port      = 0
ports       = 0
masquerade  = ""
stealth     = False
randomize   = False

def getports(a):

    global s_port
    global e_port

    s_port_pattern = r"^([0-9]+)\-"
    e_port_pattern = r"\-([0-9]+)$"

    s_port_res = re.search(s_port_pattern, a)
    e_port_res = re.search(e_port_pattern, a)

    if(s_port_res) and (e_port_res):

        s = int(s_port_res.group(1))
        e = int(e_port_res.group(1))

        if (s <= 0 or s > e or e > 65535):
            print "[-] Ports not in bound"
            sys.exit()
        else:
            s_port = s
            e_port = e 

    else:
        print "[-] Invalid ports parameters"
        sys.exit()
    

def usage():
    print "Usage:       ./portscanner.py -d [destination] -p [start-end]"
    print "Options:"
    print "             -s          Stealth scan : SYN Scan + randomized source ports"
    print "             -m [ipsrc]  Masquerade IP source with [ipsrc]"
    print ""
    print "Example:"
    print "             ./portscanner.py -d 192.168.0.2 -p 1-1024 -s"
    print "             ./portscanner.py -d 192.168.0.2 -p 1-1024 -s -m 192.168.0.3"
    sys.exit()


def scan(dest, sport, eport):
    
    if (not masquerade and not stealth):
        # Classique TCP scan
        # for i in range(sport, eport):
        #     res = sr1(IP(dst=destination)/TCP(dport=i), verbose=0, timeout=1)
        #     if res[TCP].flag == 18:   # SA
        #         print i, "      open"
        print "[*] Lvl 1 Classique Scan"
        for i in range(s_port, e_port):
            res = sr1(IP(dst=destination)/TCP(dport=i), verbose=0, timeout=1)
            if res[TCP].flags == 18:
                print str(i), "      open"
    elif (not masquerade and stealth):
        # Stealth scan : randomize src port and perform a SYN scan)
        print "[*] Lvl 2 scan (stealth)"

        for i in range(s_port, e_port):
            rand_port = random.randint(1025, 65534)
            res = sr1(IP(dst=destination)/TCP(sport=rand_port, dport=i, flags="S"), verbose=0, timeout=1)
            if res[TCP].flags == 18:
                print str(i), "      open"

    elif (masquerade and not stealth):
        # Masquerade scan : perform a scan with an IP src given as parameters
        print "[*] Lvl 3 scan (masquerade)"
        print "[*] IP src = ", masquerade
        for i in range(s_port, e_port):
            res = sr1(IP(src=masquerade, dst=destination)/TCP(dport=i), verbose=0, timeout=1)
            if res[TCP].flags == 18:
                print str(i), "      open"

    elif (masquerade and stealth):
        # Full stealth mode activate ! SYN Scan + Src ports randomized + IP source masquerade
        print "[*] Lvl 4 scan (full stealth)"
        print "[*] IP src = ", masquerade
        for i in range(s_port, e_port):
            rand_port = random.randint(1025, 65534)
            res = sr1(IP(src=masquerade, dst=destination)/TCP(sport=rand_port, dport=i), verbose=0, timeout=1)
            if res[TCP].flags == 18:
                print str(i), "      open"


def main():

    global destination
    global ports
    global masquerade
    global stealth
    global randomize

    try:
        opt, args = getopt.getopt(sys.argv[1:], "hd:p:m:s", ["help", "destination=", "ports=", "masquerade=", "stealth"])
    except getopt.GetoptError as e:
        print str(e)
        print ""
        usage()

    for o, a in opt:
            if o in ("-d", "--destination"):
                destination = a;
            elif o in ("-p", "--ports"):
                ports = a 
                try:
                    getports(a)
                except Exception, e:
                    print str(e)
                    usage()
            elif o in ("-m", "--masquerade"):
                masquerade = a
            elif o in ("-s", "--stealth"):
                stealth = True

    if (destination == "") or (ports == 0):
        usage()

    print "[*] Scanning %s [%d-%d]" % (destination, int(s_port), int(e_port))
    
    t1 = datetime.now()
    
    scan(destination, s_port, e_port)
    
    t2 = datetime.now()

    total = t2-t1

    print "[*] Scan finished in ", total

main()
