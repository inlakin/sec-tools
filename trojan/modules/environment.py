#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os

def run(**args):
    print "[=>] MODULE Environment"
    return str(os.environ)
