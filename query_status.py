#!/usr/bin/env python3

import serial
import oectrl
import sys


s=serial.Serial(sys.argv[1], baudrate=oectrl.baudrate)
addr,ch=oectrl.ch2addr(int(sys.argv[2]))
print(addr,ch)
msg=oectrl.query_single_atta(addr, ch)
oectrl.print_msg(msg)
s.write(msg)
oectrl.await_response_and_parse(s)
