#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os

def run(**args):
    print "[=>] MODULE Dirlister"
    files = os.listdir(".")

    return str(files)
