#!/usr/bin/env python3 

import crcmod
import struct
import serial
crc=crcmod.mkCrcFun(0x11021,rev=False,initCrc=0x00)

def calc_checksum(x):
    return struct.pack('<H',crc(bytes(x)))

def pack_msg(data):
    assert(len(data)-5==data[-3])
    cs=calc_checksum(data[1:])
    return bytes(data)+cs+b'\x7f'

def unpack_msg(data):
    header,addr, cmd, ack, length, *rest=data
    payload=rest[:length]
    checksum=rest[length:-1]
    assert(ack==0x00)
    assert(calc_checksum(data[1:-3])==bytes(checksum))
    assert(len(checksum)==2)
    assert(bytes(rest[-1:])==b'\x7f')
    return addr, cmd, ack, payload


def set_single_gain(addr, ch, value):
    data=[0x7e, addr, 0x20, 0x00, 0x02, ch, value]
    return pack_msg(data)

def single_gain_ack(addr, result):
    data=[0x7e, addr, 0x20, result, 0x01, 0x00]
    return pack_msg(data)


def set_all_gain(addr, gains):
    data=[0x7e, addr, 0x21, 0x00, 0x14]+gains
    return pack_msg(data)

def all_gain_ack(addr, result):
    data=[0x7e, addr, 0x21, result, 0x01, 0x00]
    return pack_msg(data)


def set_addr(addr):
    data=[0x7e, 0x00, 0x22, 0x00, 0x01, addr]
    return pack_msg(data)

def addr_ack(addr, result):
    data=[0x7e, addr, 0x22, result, 0x01, 0x00]
    return pack_msg(data)

def query_single_gain(addr, ch):
    data=[0x7e, addr, 0x11, 0x00, 0x01, ch]
    return pack_msg(data)

def single_gain_reply(addr, ch, gain, power, current, result):
    data=[0x7e, addr, 0x11, result, 0x04, ch, gain, power, current]
    return pack_msg(data)


def query_all_gain(addr):
    data=[0x7e, addr, 0x12, 0x00, 0x01, 0x00]
    return pack_msg(data)



msg=set_single_gain(11, 1, 24)
print(unpack_msg(msg))