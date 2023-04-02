#!/usr/bin/env python3

import serial
import oectrl
import sys


s=serial.Serial(sys.argv[1], baudrate=oectrl.baudrate)
oectrl.run_dummy_oe(s, 0x11)
