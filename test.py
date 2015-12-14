#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys

curpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
basename = os.path.basename(__file__)
print curpath
print basename
if curpath not in sys.path: sys.path.append(curpath)

import utils

def test(depth=0):
    frame = sys._getframe(depth)
    code = frame.f_code

    print "frame depth = ",depth
    print "func name = ", code.co_name
    print "func filename = ", code.co_filename
    print "frame lineno = ",frame.f_lineno
    print "func lineno = ",code.co_firstlineno
    print "func locals = ",frame.f_locals


def main():
    import pdb;pdb.set_trace()
    print utils.findCaller()

if __name__=="__main__":
    test(1)


