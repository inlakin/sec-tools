#! /usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import getopt
import re
import random
import logging
from datetime import datetime

logging.getLogger("scapy.runtime").setLevel(logging.ERROR) 
from scapy.all import *

destination = ""
s_port      = 0
e_port      = 0
ports       = 0
masquerade  = ""
stealth     = False
randomize   = False
closed      = 0

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


def is_up(ipdst):
    res = sr1(IP(dst=ipdst)/ICMP(), timeout=5, verbose=0)
    if not (res is None):
        return True
    else:
        return False


def scan_stealth(ipdest, sport, eport):
   
    global closed

    print "[*] Stealth scan"

    for i in range(s_port, e_port+1):
        rand_port = random.randint(1024, 65534)

        res = sr1(IP(dst=ipdest)/TCP(sport=rand_port, dport=i, flags="S"), timeout=3, verbose=0)
        
        if str(type(res)) == "<type 'NoneType'>":
            closed += 1
        elif res.haslayer(TCP):
            if res.getlayer(TCP).flags == 0x12:
                send_rsp = sr(IP(dst=ipdest)/TCP(sport=rand_port, dport=i, flags="R"), timeout=3, verbose=0)
                print str(i), "     open"
        
            elif res.getlayer(TCP).flags == 0x14:
                closed += 1


def scan_masquerade(ipdest, ipsrc, sport, eport):
    
    global closed

    print "[*] Masquerade scan"

    for i in range(s_port, e_port+1):
        rand_port = random.randint(1024, 65534)
        
        res = sr1(IP(dst=ipdest, src=ipsrc)/TCP(dport=i, flags="S"), timeout=3, verbose=0)
        
        if str(type(res)) == "<type 'NoneType'>":
            closed += 1
        elif res.haslayer(TCP):
            if res.getlayer(TCP).flags == 0x12:
                send_rsp = sr(IP(dst=ipdest, src=ipsrc)/TCP(dport=i, flags="AR"), timeout=3, verbose=0)
                print str(i), "     open"
        
            elif res.getlayer(TCP).flags == 0x14:
                closed += 1


def scan_stealth_masquerade(ipdest, ipsrc, sport, eport):
    
    global closed 

    print "[*] Stealth masquerade scan"
    for i in range(s_port, e_port+1):
        rand_port = random.randint(1024, 65534)
        
        res = sr1(IP(dst=ipdest, src=ipsrc)/TCP(sport=rand_port, dport=i, flags="S"), timeout=3, verbose=0)
        
        if str(type(res)) == "<type 'NoneType'>":
            closed += 1
        elif res.haslayer(TCP):
            if res.getlayer(TCP).flags == 0x12:
                send_rsp = sr(IP(dst=ipdest, src=ipsrc)/TCP(sport=rand_port, dport=i, flags="AR"), timeout=3, verbose=0)
                print str(i), "     open"
        
            elif res.getlayer(TCP).flags == 0x14:
                closed += 1


def scan(dest, sport, eport):
    
    global closed 

    print "[*] Classique Scan"

    for i in range(s_port, e_port+1):
        res = sr1(IP(dst=destination)/TCP(dport=i), verbose=0, timeout=3)

        if str(type(res)) == "<type 'NoneType'>":
            closed  += 1
        elif res.haslayer(TCP):
            if res.getlayer(TCP).flags == 0x12:
                send_rsp = sr(IP(dst=destination)/TCP(dport=i, flags='AR'), verbose=0, timeout=3)
                print str(i), "      open"
            elif res.getlayer(TCP).flags == 0x14:
                closed += 1


def main():

    global destination
    global ports
    global masquerade
    global stealth
    global randomize

    host_up = False

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

    if is_up(destination):
        host_up = True
    else:
        host_up = False

    if host_up:
        print "[*] Scanning %s [%d-%d]" % (destination, int(s_port), int(e_port))
        t1 = datetime.now()
        
        if not stealth and not masquerade:
            scan(destination, s_port, e_port)

        elif stealth and not masquerade:
            scan_stealth(destination, s_port, e_port)

        elif not stealth and masquerade:
            scan_masquerade(destination, masquerade, s_port, e_port)

        elif stealth and masquerade:
            scan_stealth_masquerade(destination, masquerade, s_port, e_port)
        
        t2 = datetime.now()

        total = t2 - t1
        print "[*] %d ports closed " % closed
        print "[*] Scan finished in ", total

    else:
        print "[-] Host %s seems down" % destination    

main()
