#!/usr/bin/env python3 

import crcmod
import struct
import serial
import time
crc=crcmod.mkCrcFun(0x11021,rev=False,initCrc=0x00)

baudrate=57600

def calc_checksum(x):
    return struct.pack('<H',crc(bytes(x)))

def pack_msg(data):
    assert(len(data)-5==data[4])
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

def await_cmd(port):
    while port.inWaiting()==0:
        time.sleep(0.5)
    cmd=port.read_all()
    print("raw bytes:")
    print_msg(cmd)
    return unpack_msg(cmd)

def respond_cmd(addr, cmd, payload):
    result=0x00
    if cmd==0x20:
        return single_atta_ack(addr, result)
    elif cmd==0x21:
        return all_atta_ack(addr, result)
    elif cmd==0x22:
        return addr_ack(addr, result)
    elif cmd==0x11:
        return single_atta_reply(addr, payload[0], 44,55,66, result)
    else:
        raise NotImplementedError


def await_response(port):
    while port.inWaiting()==0:
        time.sleep(0.5)
    response=port.read_all()
    print("response raw message:")
    print_msg(response)
    return unpack_msg(response[:-1])

def parse_response(addr, cmd, ack, payload):
    if cmd==0x20:
        print("Ack of set single atta:{0}".format(ack))
    elif cmd==0x21:
        print("Ack of set all atta:{0}".format(ack))
    elif cmd==0x22:
        print("Ack of address setting:{0} {1}".format(ack, addr))
    elif cmd==0x11:
        ch, atta, power, current=payload
        print("Ack of status of ch {0}:{1} atta={2} power={3} current={4}".format(addr, ch, atta, power, current))
    else:
        raise NotImplementedError

def await_response_and_parse(port):
    addr, cmd, ack, payload=await_response(port)
    parse_response(addr, cmd, ack, payload)


def set_single_atta(addr, ch, value):
    data=[0x7e, addr, 0x20, 0x00, 0x02, ch, value]
    return pack_msg(data)

def single_atta_ack(addr, result):
    data=[0x7e, addr, 0x20, result, 0x01, 0x00]
    return pack_msg(data)


def set_all_atta(addr, attas):
    data=[0x7e, addr, 0x21, 0x00, 0x14]+attas
    return pack_msg(data)

def all_atta_ack(addr, result):
    data=[0x7e, addr, 0x21, result, 0x01, 0x00]
    return pack_msg(data)


def set_addr(addr):
    data=[0x7e, 0x00, 0x22, 0x00, 0x01, addr]
    return pack_msg(data)

def addr_ack(addr, result):
    data=[0x7e, addr, 0x22, result, 0x01, 0x00]
    return pack_msg(data)

def query_single_atta(addr, ch):
    data=[0x7e, addr, 0x11, 0x00, 0x01, ch]
    return pack_msg(data)

def single_atta_reply(addr, ch, atta, power, current, result):
    data=[0x7e, addr, 0x11, result, 0x04, ch, atta, power, current]
    return pack_msg(data)

def ch2addr(ch):
    if ch<=20:
        return 0x11,ch
    elif ch>=21 and ch<=40:
        return 0x12, ch-20
    else:
        raise RuntimeError("ch {0} out of range".format(ch))

def query_all_atta(addr):
    data=[0x7e, addr, 0x12, 0x00, 0x01, 0x00]
    return pack_msg(data)

def run_dummy_oe(port, addr):
    while True:
        addr, cmd, ack, payload=await_cmd(port)
        print("decoded cmd:")
        print("0x{0:X} 0x{1:X} {2} {3}".format(addr, cmd, ack, payload))
        port.write(respond_cmd(addr, cmd, payload))

def print_msg(msg):
    print(" ".join(["0x%02x"%(i) for i in msg]))
