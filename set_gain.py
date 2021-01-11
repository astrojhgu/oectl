#!/usr/bin/env python3

import serial
import oectrl
import sys


s=serial.Serial(sys.argv[1], baudrate=oectrl.baudrate)
addr,ch=oectrl.ch2addr(int(sys.argv[2]))
gain=int(sys.argv[3])

s.write(oectrl.set_single_gain(addr, ch ,gain))
oectrl.await_response_and_parse(s)
