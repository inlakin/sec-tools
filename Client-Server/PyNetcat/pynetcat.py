#! /usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import socket
import getopt
import threading
import subprocess
import paramiko
import re

from termcolor import colored

listen      = False
port        = 0
destination = ""
shell       = False
encrypt     = False
ssh_auth    = ""
ssh_user    = ""
ssh_passwd  = ""

class SSH_Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, user, passwd):
        if user == ssh_user and passw == ssh_passwd:
            return paramiko.AUTH_SUCCESSFUL

        return paramiko.AUTH_FAILED
def ssh_parse_auth(auth):
    pat = r"([\w]+),([\w]+)"
    res = re.search(pat,auth)
    if res:
        return res.group(1), res.group(2)
    else:
        print "[!] Failed parsing SSH credentials"
        sys.exit(1)
def ssh_init():
    global ssh_user
    global ssh_passwd
    global ssh_port
    
    ssh_user, ssh_passwd = ssh_parse_auth(ssh_auth)
    print "[*] SSH initialized with USER " + ssh_user + " PASS " + ssh_passwd
def ssh_server():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((destination, port))
    s.listen(1)

    ssh_init()

    print "[+] Listening for connection ..."

    try:
        ssh_client, ssh_client_addr = s.accept()
    except Exception, e:
        print "[!] Listen failed " + str(e)
        return False

    print "[*] Connection established with " + ssh_client_addr[0] + ":" + str(ssh_client_addr[1]) + "."

    ssh_session = paramiko.Transport(client)
    server = SSH_Server()
    try:
        ssh_session.start_server(server=server)
    except paramiko.SSHException, x:
        print "[!] SSH negociation failed"

    chan = ssh_session.accept(20)
    print "[*] SSH: authentication successful"
    print chan.recv(1024)
    chan.send("=== SSH CONFIGURED ===")



    return True
def ssh_command(ip, user, passwd, cmd):
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, username=user, password=passwd)
            ssh_session = client.get_transport().open_session()
            
            if ssh_session.active:
                ssh_session.exec_command(cmd)
                print ssh_session.recv(1024)
            return
        except Exception, e:
            print "[!] Failed to connect to " + user + "@" + ip
            print "[!] Exception : " + str(e)
            sys.exit(0)
def ssh_client():
    username = raw_input("SSH Username> ")
    password = raw_input('SSH Password> ')
    
    ssh_client_auth = username +","+password

    print "[*] Connecting to %s:%d ..." % (destination, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((destination, port))
        print "[*] Connected"
        print "[*] Initializing SSH connection with USER " + username + " PASS " + password

        s.send(ssh_client_auth)
        data = s.recv(1024)

        if "Failed" in data:
            print "[!] Credentials failed"
            sys.exit(0)
        else:
            print "[*] SSH Connection established"
            while True:
                recv_len = 1 
                data = s.recv(4096)
                res += data

                if recv_len < 4096:
                    break

                print res,

                cmd = raw_input()
                cmd += "\n"
                s.send(cmd)

    except Exception as e:
        print str(e)
        sys.exit(1)


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
    print "         -c, --bind-shell  initialize a bind shell"

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
            
            try:
                cmd = raw_input()
                cmd += "\n"
                s.send(cmd)
            except KeyboardInterrupt:
                print "\r\n[*] Ctrl+C received. Exiting."
                s.close()
                sys.exit(0)

    except Exception, e:
        print str(e)
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
        s.close()
        sys.exit(0)

def main():
    
    global listen
    global port 
    global destination
    global shell
    global encrypt
    global ssh_auth

    try:
        opt, args = getopt.getopt(sys.argv[1:], "hlp:d:se:", ["help", "listen", "port", "destination","shell", "encrypt="])
    except getopt.GetoptError as e:
        print str(e)        
        print ""
        usage()
        print sys.exit(0)

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
        elif o in ("-e", "--encrypt"):
            encrypt = True
            ssh_auth = a 
        else:
            print "[*] Option is not handled"
    
    if port == 0:
        print "[*] You're missing something, John.."
        print ""
        usage()
        sys.exit(0)

    if not listen and len(destination) and port > 0 and not encrypt:
        print "--------------------------"
        print "-                        -"
        print "-   PyNetcat : CLIENT    -"
        print "-                        -"
        print "--------------------------"
        print ""
        client()
    elif not listen and len(destination) and port > 0 and encrypt:
        print "------------------------------"
        print "-                            -"
        print "-   PyNetcat : SSH-CLIENT    -"
        print "-                            -"
        print "------------------------------"
        print ""
        ssh_client()
    elif listen and port > 0 and not encrypt:
        print "--------------------------"
        print "-                        -"
        print "-   PyNetcat : SERVER    -"
        print "-                        -"
        print "--------------------------"
        print ""
        server()
    elif listen and encrypt:
        print "-----------------------------"
        print "-                           -"
        print "-   PyNetcat : SSH-SERVER   -"
        print "-                           -"
        print "-----------------------------"
        print ""
        ssh_server()

main()

