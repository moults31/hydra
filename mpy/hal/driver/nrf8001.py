#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""DNRF8001 driver for Micro Python"""

__author__ = "Joachim"
__copyright__ = "Copyright 2007, .."
__credits__ = ["Joachim",]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Joachim"
__email__ = "jobbyworld@free.fr"
__status__ = "Develloppement"

# SPDX-FileCopyrightText: 2022 Zac Moulton
#
# SPDX-License-Identifier: MIT

msgs=[
    [ 0x07, 0x06, 0x00, 0x00, 0x03, 0x02, 0x42, 0x07 ],
    [ 0x1F, 0x06, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0B, 0x00, 0x0D, 0x01, 0x01, 0x00, 0x00, 0x06, 0x00, 0x00, 0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
    [ 0x1F, 0x06, 0x10, 0x1C, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x14, 0x00, 0x90, 0x01, 0xFF ],
    [ 0x1F, 0x06, 0x10, 0x38, 0xFF, 0xFF, 0x02, 0x58, 0x0A, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
    [ 0x05, 0x06, 0x10, 0x54, 0x00, 0x00 ],
    [ 0x1F, 0x06, 0x20, 0x00, 0x04, 0x04, 0x02, 0x02, 0x00, 0x01, 0x28, 0x00, 0x01, 0x00, 0x18, 0x04, 0x04, 0x05, 0x05, 0x00, 0x02, 0x28, 0x03, 0x01, 0x0E, 0x03, 0x00, 0x00, 0x2A, 0x04, 0x14, 0x05 ],
    [ 0x1F, 0x06, 0x20, 0x1C, 0x05, 0x00, 0x03, 0x2A, 0x00, 0x01, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x04, 0x04, 0x05, 0x05, 0x00, 0x04, 0x28, 0x03, 0x01, 0x02, 0x05, 0x00, 0x01, 0x2A, 0x06, 0x04, 0x03 ],
    [ 0x1F, 0x06, 0x20, 0x38, 0x02, 0x00, 0x05, 0x2A, 0x01, 0x01, 0x80, 0x00, 0x04, 0x04, 0x05, 0x05, 0x00, 0x06, 0x28, 0x03, 0x01, 0x02, 0x07, 0x00, 0x04, 0x2A, 0x06, 0x04, 0x09, 0x08, 0x00, 0x07 ],
    [ 0x1F, 0x06, 0x20, 0x54, 0x2A, 0x04, 0x01, 0x0A, 0x00, 0x12, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x04, 0x04, 0x02, 0x02, 0x00, 0x08, 0x28, 0x00, 0x01, 0x01, 0x18, 0x04, 0x04, 0x05, 0x05, 0x00, 0x09 ],
    [ 0x1F, 0x06, 0x20, 0x70, 0x28, 0x03, 0x01, 0x22, 0x0A, 0x00, 0x05, 0x2A, 0x26, 0x04, 0x05, 0x04, 0x00, 0x0A, 0x2A, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x46, 0x14, 0x03, 0x02, 0x00, 0x0B, 0x29 ],
    [ 0x1F, 0x06, 0x20, 0x8C, 0x02, 0x01, 0x00, 0x00, 0x04, 0x04, 0x02, 0x02, 0x00, 0x0C, 0x28, 0x00, 0x01, 0x0A, 0x18, 0x04, 0x04, 0x05, 0x05, 0x00, 0x0D, 0x28, 0x03, 0x01, 0x02, 0x0E, 0x00, 0x27 ],
    [ 0x1F, 0x06, 0x20, 0xA8, 0x2A, 0x04, 0x04, 0x09, 0x01, 0x00, 0x0E, 0x2A, 0x27, 0x01, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x05, 0x05, 0x00, 0x0F, 0x28, 0x03, 0x01 ],
    [ 0x1F, 0x06, 0x20, 0xC4, 0x0E, 0x10, 0x00, 0x29, 0x2A, 0x44, 0x14, 0x14, 0x02, 0x00, 0x10, 0x2A, 0x29, 0x01, 0x30, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
    [ 0x1F, 0x06, 0x20, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x05, 0x05, 0x00, 0x11, 0x28, 0x03, 0x01, 0x02, 0x12, 0x00, 0x24, 0x2A, 0x04, 0x04, 0x08, 0x02, 0x00, 0x12, 0x2A, 0x24 ],
    [ 0x1F, 0x06, 0x20, 0xFC, 0x01, 0x31, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x05, 0x05, 0x00, 0x13, 0x28, 0x03, 0x01, 0x02, 0x14, 0x00, 0x26, 0x2A, 0x04, 0x04, 0x04, 0x02, 0x00 ],
    [ 0x1F, 0x06, 0x21, 0x18, 0x14, 0x2A, 0x26, 0x01, 0x33, 0x34, 0x00, 0x00, 0x04, 0x04, 0x05, 0x05, 0x00, 0x15, 0x28, 0x03, 0x01, 0x02, 0x16, 0x00, 0x50, 0x2A, 0x06, 0x04, 0x08, 0x07, 0x00, 0x16 ],
    [ 0x1F, 0x06, 0x21, 0x34, 0x2A, 0x50, 0x01, 0x02, 0x00, 0x00, 0xAA, 0xAA, 0xCC, 0xCC, 0x04, 0x04, 0x10, 0x10, 0x00, 0x17, 0x28, 0x00, 0x01, 0x9E, 0xCA, 0xDC, 0x24, 0x0E, 0xE5, 0xA9, 0xE0, 0x93 ],
    [ 0x1F, 0x06, 0x21, 0x50, 0xF3, 0xA3, 0xB5, 0x01, 0x00, 0x40, 0x6E, 0x04, 0x04, 0x13, 0x13, 0x00, 0x18, 0x28, 0x03, 0x01, 0x04, 0x19, 0x00, 0x9E, 0xCA, 0xDC, 0x24, 0x0E, 0xE5, 0xA9, 0xE0, 0x93 ],
    [ 0x1F, 0x06, 0x21, 0x6C, 0xF3, 0xA3, 0xB5, 0x02, 0x00, 0x40, 0x6E, 0x44, 0x10, 0x14, 0x00, 0x00, 0x19, 0x00, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
    [ 0x1F, 0x06, 0x21, 0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x13, 0x13, 0x00, 0x1A, 0x28, 0x03, 0x01, 0x10, 0x1B, 0x00, 0x9E, 0xCA, 0xDC, 0x24, 0x0E, 0xE5, 0xA9, 0xE0 ],
    [ 0x1F, 0x06, 0x21, 0xA4, 0x93, 0xF3, 0xA3, 0xB5, 0x03, 0x00, 0x40, 0x6E, 0x14, 0x00, 0x14, 0x00, 0x00, 0x1B, 0x00, 0x03, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
    [ 0x1F, 0x06, 0x21, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46, 0x14, 0x03, 0x02, 0x00, 0x1C, 0x29, 0x02, 0x01, 0x00, 0x00, 0x04, 0x04, 0x13, 0x13, 0x00, 0x1D, 0x28, 0x03 ],
    [ 0x1F, 0x06, 0x21, 0xDC, 0x01, 0x14, 0x1E, 0x00, 0x9E, 0xCA, 0xDC, 0x24, 0x0E, 0xE5, 0xA9, 0xE0, 0x93, 0xF3, 0xA3, 0xB5, 0x04, 0x00, 0x40, 0x6E, 0x54, 0x10, 0x09, 0x00, 0x00, 0x1E, 0x00, 0x04 ],
    [ 0x1F, 0x06, 0x21, 0xF8, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46, 0x14, 0x03, 0x02, 0x00, 0x1F, 0x29, 0x02, 0x01, 0x00, 0x00, 0x04, 0x04, 0x13, 0x13, 0x00, 0x20, 0x28 ],
    [ 0x1F, 0x06, 0x22, 0x14, 0x03, 0x01, 0x02, 0x21, 0x00, 0x9E, 0xCA, 0xDC, 0x24, 0x0E, 0xE5, 0xA9, 0xE0, 0x93, 0xF3, 0xA3, 0xB5, 0x05, 0x00, 0x40, 0x6E, 0x06, 0x04, 0x07, 0x06, 0x00, 0x21, 0x00 ],
    [ 0x0C, 0x06, 0x22, 0x30, 0x05, 0x02, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00 ],
    [ 0x1F, 0x06, 0x40, 0x00, 0x2A, 0x00, 0x01, 0x00, 0x80, 0x04, 0x00, 0x03, 0x00, 0x00, 0x2A, 0x05, 0x01, 0x00, 0x04, 0x04, 0x00, 0x0A, 0x00, 0x0B, 0x2A, 0x27, 0x01, 0x00, 0x80, 0x04, 0x00, 0x0E ],
    [ 0x1F, 0x06, 0x40, 0x1C, 0x00, 0x00, 0x2A, 0x29, 0x01, 0x00, 0x90, 0x04, 0x00, 0x10, 0x00, 0x00, 0x2A, 0x24, 0x01, 0x00, 0x80, 0x04, 0x00, 0x12, 0x00, 0x00, 0x2A, 0x26, 0x01, 0x00, 0x80, 0x04 ],
    [ 0x1F, 0x06, 0x40, 0x38, 0x00, 0x14, 0x00, 0x00, 0x2A, 0x50, 0x01, 0x00, 0x80, 0x04, 0x00, 0x16, 0x00, 0x00, 0x00, 0x02, 0x02, 0x00, 0x08, 0x04, 0x00, 0x19, 0x00, 0x00, 0x00, 0x03, 0x02, 0x00 ],
    [ 0x1D, 0x06, 0x40, 0x54, 0x02, 0x04, 0x00, 0x1B, 0x00, 0x1C, 0x00, 0x04, 0x02, 0x00, 0x0A, 0x04, 0x00, 0x1E, 0x00, 0x1F, 0x00, 0x05, 0x02, 0x00, 0x80, 0x04, 0x00, 0x21, 0x00, 0x00 ],
    [ 0x13, 0x06, 0x50, 0x00, 0x9E, 0xCA, 0xDC, 0x24, 0x0E, 0xE5, 0xA9, 0xE0, 0x93, 0xF3, 0xA3, 0xB5, 0x00, 0x00, 0x40, 0x6E ],
    [ 0x1F, 0x06, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
    [ 0x08, 0x06, 0x60, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00 ],
    [ 0x06, 0x06, 0xF0, 0x00, 0x03, 0x65, 0xF7 ],
        ]

CMDS =  {1: 'TEST',
         2: 'ECHO',
         3: 'DTM_CMD',
         4: 'SLEEP',
         5: 'WAKEUP',
         6: 'SETUP',
         7: 'READ_DYNAMIC_DATA',
         8: 'WRITE_DYNAMIC_DATA',
         9: 'GET_DEVICE_VERSION',
         10: 'GET_DEVICE_ADDRESS',
         11: 'GET_BATTERY_LEVEL',
         12: 'GET_TEMPERATURE',
         13: 'SET_LOCAL_DATA',
         14: 'RADIO_RESET',
         15: 'CONNECT',
         16: 'BOND',
         17: 'DISCONNECT',
         18: 'SET_TX_POWER',
         19: 'CHANGE_TIMING',
         20: 'OPEN_REMOTE_PIPE',
         21: 'SEND_DATA',
         22: 'SEND_DATA_ACK',
         23: 'REQUEST_DATA',
         24: 'SEND_DATA_NACK',
         25: 'SET_APP_LATENCY',
         26: 'SET_KEY',
         27: 'OPEN_ADV_PIPE',
         28: 'BROADCAST',
         29: 'BOND_SECURITY_REQUEST',
         30: 'CONNECT_DIRECT',
         31: 'CLOSE_REMOTE_PIPE',
         255: 'INVALID'}
EVTS =   {0: 'INVALID',
         129: 'DEVICE_STARTED',
         130: 'ECHO',
         131: 'HW_ERROR',
         132: 'CMD_RSP',
         133: 'CONNECTED',
         134: 'DISCONNECTED',
         135: 'BOND_STATUS',
         136: 'PIPE_STATUS',
         137: 'TIMING',
         138: 'DATA_CREDIT',
         139: 'DATA_ACK',
         140: 'DATA_RECEIVED',
         141: 'PIPE_ERROR',
         142: 'DISPLAY_PASSKEY',
         143: 'KEY_REQUEST'}
STATUS   = {0: 'SUCCESS',
            1: 'TRANSACTION_CONTINUE',
            2: 'TRANSACTION_COMPLETE',
            3: 'EXTENDED',
            128: 'ERROR_UNKNOWN',
            129: 'ERROR_INTERNAL',
            130: 'ERROR_CMD_UNKNOWN',
            131: 'ERROR_DEVICE_STATE_INVALID',
            132: 'ERROR_INVALID_LENGTH',
            133: 'ERROR_INVALID_PARAMETER',
            134: 'ERROR_BUSY',
            135: 'ERROR_INVALID_DATA',
            136: 'ERROR_CRC_MISMATCH',
            137: 'ERROR_UNSUPPORTED_SETUP_FORMAT',
            138: 'ERROR_INVALID_SEQ_NO',
            139: 'ERROR_SETUP_LOCKED',
            140: 'ERROR_LOCK_FAILED',
            141: 'ERROR_BOND_REQUIRED',
            142: 'ERROR_REJECTED',
            143: 'ERROR_DATA_SIZE',
            144: 'ERROR_PIPE_INVALID',
            145: 'ERROR_CREDIT_NOT_AVAILABLE',
            146: 'ERROR_PEER_ATT_ERROR',
            147: 'ERROR_ADVT_TIMEOUT',
            148: 'ERROR_PEER_SMP_ERROR',
            149: 'ERROR_PIPE_TYPE_INVALID',
            150: 'ERROR_PIPE_STATE_INVALID',
            151: 'ERROR_INVALID_KEY_SIZE',
            152: 'ERROR_INVALID_KEY_DATA',
            240: 'RESERVED_START',
            255: 'RESERVED_END'}

import sys

print(sys.platform)

import time

#from nrf_parsers import parse_service,
#msgs = parse_service()


import machine
import struct
from machine import Pin, SPI

"""
Micro Python implements the entire Python 3.4 syntax 
(including exceptions, "with", "yield from", etc.). 
The following core datatypes are provided: 
str (including basic Unicode support), 
bytes, bytearray, 
tuple, list, dict, set, frozenset, 
array.array, collections.namedtuple, classes and instances. 
Builtin modules include sys, time, and struct. 
Note that only subset of Python 3.4 functionality implemented for the data types and modules.
"""

CONFIG      = const(0x00)
def format_event(_event):
    def toTable(bitmap):
            po=map("{0:0>8b}".format,bitmap)
            po=map(reversed,po)
            po=map("".join,po)
            po="".join(po)
            return po
    evt_code=_event[0]
    if evt_code == 0x84:
        CommandOpCode=_event[1]
        status_code=_event[2]
        return "{0} {1} {2}".format(EVTS.get(evt_code),CMDS.get(CommandOpCode),STATUS.get(status_code),_event[3:])
    elif evt_code == 0x81:
        # OperatingMode 
        # 0x01 Test
        # 0x02 Setup
        # 0x03 Standby
        # HWError 0x00 No error
        # 0x01 Fatal error
        # DataCreditAvailable 00 Number of DataCommand buffers available
        OperatingMode={0x01:"Test",0x02:"Setup",0x03:"Standby"}.get(_event[1])
        HWError={0x00:"No Error",0x01:"Fatal Error"}.get(_event[2])
        DataCreditAvailable=int(_event[3])
        return "{0} {1} {2} Data Credit {3}".format(EVTS.get(evt_code),OperatingMode,HWError,DataCreditAvailable)
    elif evt_code == 0x8D:
        pipe=_event[1]
        
        
        return "{0} on #{1} : {2}".format(EVTS.get(evt_code),pipe,STATUS.get(_event[2]))
    elif evt_code == 0X88:
        data_event=_event[1:]
        o=toTable(data_event[0:8])
        c=toTable(data_event[8:16])

        return "PIPES STATUS:\n\tO:{0}\n\tC:{1}".format(o,c)
    else:
        return "{0} {1}".format(EVTS.get(evt_code),list(map(hex,_event)))


i=0
char_buffer=bytearray(1)
import struct
    #print(struct.unpack('BBBB',b'\x81\x02\x00\x02'))
    

class NRF8001:
    def __init__(self, spi, req, rdy, act, rst, debug=True):
        # init the SPI bus and pins
        #spi.init(mode, baudrate=328125, *, prescaler, polarity=1, phase=0, bits=8, firstbit=SPI.MSB, ti=False, crc=None)
        spi.init(baudrate=2000000, polarity=0, phase=0, bits=8)
        
        req.init(req.OUT, None) #rqt on low     
        rdy.init(rdy.IN,rdy.PULL_UP) # rdy on low
        self.debug=debug
        if rst:
            rst.init(req.OUT, None) #rqt on low
        # store the pins
        self.spi = spi
        self.req = req
        self.rdy = rdy
        self.rst=rst
        self.led=Pin("LED", Pin.OUT)
        # reset everything
        self.rst.high()
        self.req.high()
        time.sleep(0.5)
        self.PipesOpen=b"0"*64
        self.PipesClosed=b"0"*64
        self.DataCreditAvailable=0

    def __repr__(self):
        """"""
        return "<NRF8001> rdy {},req {}".format(self.rdy.value(),self.req.value())
    
    def setup(self,msgs):
        #direct send to spi (length and cmd (0x06) yet configure)
        print("Do Setup")
        for msg in msgs:
            events=self._send_cmd(msg)
            for event in events:
                if self.debug:
                    if event==b'\x84\x06\x01':
                        print("Setup Continue...")
                    else:
                        print("Unknow:",event)
        if self.debug:        
            print("Waiting setup Done")
        time.sleep(0.5)

        wait_cycle=2
        while 1:
            event = self.peek_event()
            if event ==b'\x84\x06\x02':
                if self.debug:
                    print("Setup Complete!")
            elif event==b'\x84\x06\x01':
                if self.debug:
                    print("Setup Continue...")
            else:
                wait_cycle-=1
                time.sleep(0.2)
                print("...")
                if not(wait_cycle):
                    break

    def _test(self):
        # print("DO SETUP",self.cmd_test())
        print("DO echo",self.cmd_echo("coucou"))
        # print("DO SETUP",self.cmd_test(0xFF))            
    
    def reset(self):
        self.rst.high()
        self.rst.low()
        self.rst.high()
        time.sleep(0.5)
        if self.debug:
            print("reset Done")        
    
    def send_cmd(self,cmd,data=b''):
        """Send cml and compute msg to send"""
        _cmd=b"{}{}{}".format(chr(len(data)+1),chr(cmd),data)
        if self.debug:
            print ("CMD:",_cmd)
        return self._send_cmd(_cmd)

    def _send_cmd(self,cmd):
        """ 1. The application controller requests the right to send data by setting the REQN pin to ground.
            2. nRF8001 sets the RDYN pin to ground when it is ready to receive data.
            3. The application controller starts sending data on the MOSI pin:
            • Byte 1 (length byte) from the application controller defines the length of the message.
            • Byte 2 (ACI byte1) is the first byte of the ACI data.
            • Byte N is the last byte of the ACI data.
            • The application controller sets the REQN pin high to terminate the data transaction.
            Note: The maximum length of a command packet is 32 bytes, including the length byte. MOSI shall
            be held low if the application controller receives an event and has no message to send to the
            nRF8001.
        
            nRF8001 is capable of receiving an ACI command simultaneously as it sends an ACI event to the
            application controller.
            The application controller shall always read the length byte from nRF8001 and check if the length is
            greater than 0. If the length is greater than 0 the data on the MISO line shall be read as described in
            section 7.1.5.
            An ACI event received from the nRF8001 processor is never a reply to a command being simultaneously
            transmitted. For all commands, the corresponding event will always be received in a subsequent ACI
            transaction.
        """
        #self.extint.disable()
        
        events=list()
        event=None
        self.req.low()
        while self.rdy.value()!=0:
            pass
        mode=0
        event=b''
        dummy=None
        length=None
        for b in cmd:
            dummy = self.spi.write(b"{}".format(b))
            #print("send_recv",repr(b),repr(dummy),mode)
            if (mode==0) and (dummy==b'\x01'):
                mode=1
            elif mode == 1: #waiting length
                length = ord(dummy) 
                if length:
                    mode=2
                else:
                    mode=0
            elif mode == 2: #waiting data
                event+=dummy
                length-=1
            if length==0:
                mode=0
                if event:
                    #yield event # block execution
                    events.append(event)
                    self._on_event(event)
                event=b''   
        if length:
                event+=self.spi.read(length)
                #yield event 
                self._on_event(event)
                events.append(event)
        self.req.high()
        return events
       
    def _on_event(self,event):
        """The application controller receives the ACI event by performing the following procedure:
            1. nRF8001 sets the RDYN pin to ground.
            2. The application controller sets the REQN pin to ground and starts clocking on the SCK pin.
            • Byte 1 (debug byte) from nRF8001 is an internal debug byte and the application
            controller discards it.
            • Byte 2 (length byte) from nRF8001 defines the length of the message.
            • Byte 3 (ACI byte1) is the first byte of the ACI data.
            • Byte N is the last byte of the ACI data.
            3. The application controller sets the REQN pin high to close the event.
            Note: The maximum length of an event packet is 31 bytes, including the length byte.
        """
        if self.debug and event[0] != 0xFF:
            print("_ON_EVENT",format_event(event))
        evt_code = event[0]
        
        data_event = event[1:]
        if evt_code == 0x81:
            self._on_DEVICE_STARTED(*struct.unpack("BBB",data_event))
        elif evt_code == 0x82:
            self.on_ECHO(data_event)
        elif evt_code == 0x83:
            self.on_HW_ERROR(data_event[:2],data_event[2:])
        elif evt_code == 0x84:
            self.on_CMD_RSP(data_event[0],data_event[1],data_event[2:])
            if event==b'\x84\x06\x02':
                self.on_SETUP_COMPLETED()
            elif event==b'\x84\x06\x01':
                self.on_SETUP_CONTINUE()

        elif evt_code == 0x85:
            self.on_CONNECTED(data_event[0],data_event[1:7],data_event[7:9],data_event[9:11],data_event[11:13],data_event[13])
        elif evt_code == 0x86:
            self.on_DISCONNECTED(*struct.unpack("BB",data_event))
        elif evt_code == 0x87:
            self.on_BOND_STATUS(*struct.unpack("BBBBBB",data_event))
        elif evt_code == 0x88:
            self.on_PIPE_STATUS(data_event[0:8],data_event[8:])
        elif evt_code == 0x89:
            self.on_TIMING(*struct.unpack("HHH",data_event))
        elif evt_code == 0x8A:
            self._on_DATA_CREDIT(*struct.unpack("B",data_event))
        elif evt_code == 0x8B:
            self.on_DATA_ACK(data_event)
        elif evt_code == 0x8C:
            self.on_DATA_RECEIVED(data_event[0],data_event[1:])
        elif evt_code == 0x8D:
            self.on_PIPE_ERROR(data_event[0],int(data_event[1]),data_event[2:])
        elif evt_code == 0x8E:
            self.on_DISPLAY_PASSKEY(data_event)
        elif evt_code == 0x8F:
            self.on_KEY_REQUEST(data_event)
        elif evt_code == 0xFF:
            pass
        else:
            print("UNKNOWN EVENT")


        
    def peek_event(self):
        """
        Send active commande (buffer)
        Read event
        retrun when all done
        """
        #wait for ready
        #assert self.req.value()==1

        if self.rdy.value()==1:return
        event=None
        self.req.low()
        dummy = self.spi.read(1) 
        length = ord(self.spi.read(1))
        if length:
            event = self.spi.read(length)
        self.req.high()
        if event:
            self._on_event( event )  
        return event
    
    # _____________CMDS______________

    def cmd_test(self,TestFeature=0x02):
        """
        X01
        TestFeature 0x01 Enable DTM over UART interface
                    0x02 Enable DTM over ACI
                    0xFF Exit test mode
        """
        return self.send_cmd(0x01,[TestFeature])
            
    def cmd_echo(self,msg):
        """"""
        return self.send_cmd(0x02,msg)
        
    def cmd_DtmCommand(self):
        """"""
        pass

    def cmd_Sleep(self):
        """"""
        pass

    def cmd_Wakeup(self):
        """"""
        pass

    def cmd_Setup(self):
        """"""
        pass

    def cmd_ReadDynamicData(self):
        """"""
        pass

    def cmd_WriteReadDynamicData(self):
        """"""
        pass

    def cmd_GetDeviceVersion(self):
        """"""
        return self.send_cmd(0x09)

    def cmd_GetDeviceAddress(self):
        """"""
        return self.send_cmd(0x0A)
    
    def cmd_GetBatteryLevel(self):
        """"""
        return self.send_cmd(0x0B)
    
    def cmd_GetTemperature(self):
        """"""
        return self.send_cmd(0x0C)
    
    def cmd_RadioReset(self):
        """"""
        return self.send_cmd(0x0E)
    
    def cmd_ChangeTimingRequest(self):
        """"""
        return self.send_cmd(0x13)
        
    def cmd_connect(self,Timeout=None,AdvInterval=None):
        """
        x0F
        Timeout 0x0000 Infinite advertisement, no timeout
        If required, the RadioReset command will abort the continous
        advertisement and return nRF8001 to Standby mode
        1-16383 (0x3FFF) Valid timeout range in seconds
        AdvInterval 32 - 16384
        (0x0020 to 0x4000)
        Advertising
        hello : ,b'\x05\x0F\x00\x00\x00\x50'
        """
        return self._send_cmd(b'\x05\x0F\x00\x00\x50\x00')
        #return self.send_cmd(0x0F,b'\x00\x00\x50\x00')
     
    def cmd_OpenRemotePipe(self,pipeNumber):
        """"""
        return self._send_cmd(bytes([2,0x05,pipeNumber]))

    def cmd_OpenAdvPipe(self,AdvServiceDataPipes):
        """"""
        raise Exception("Not Implemented")

    def cmd_Broadcast(self):
        """"""
        raise Exception("Not Implemented")

    def cmd_SetLocalData(self,ServicePipeNumber,Data):
        self._send_cmd(
            bytes(  [len(Data)+2,
                    0x0D,
                    ServicePipeNumber])+Data)

    def cmd_SendData(self,ServicePipeNumber,Data):
        assert isinstance(Data,bytes)
        if self.DataCreditAvailable>0:
            self._send_cmd(
                bytes(  [len(Data)+2,
                        0x15,
                        ServicePipeNumber])+Data)
            self.DataCreditAvailable-=1
        else:
            print("NO DATA CREDIT AVAILABLE")
        if self.debug:
            print("DataCreditAvailable",self.DataCreditAvailable)
    
    # _____________END CMDS______________
    #------------------- EVENTS -------------        
    def on_INVALID(self,*args):
        """
        """
        pass

    def _on_DEVICE_STARTED(self,OperatingMode,HWError,DataCreditAvailable):
        """ keep this event to internaly set DataCreditAvailable"""
        self.DataCreditAvailable=int(DataCreditAvailable)
        self.on_DEVICE_STARTED(OperatingMode,HWError,DataCreditAvailable)
    
    def on_DEVICE_STARTED(self,OperatingMode,HWError,DataCreditAvailable):
        """ 
            OperatingMode 1 Current device mode
            HWError 1 Cause of the restart
            DataCreditAvailable
        """
        OperatingMode={0x01:"Test",0x02:"Setup",0x03:"Standby"}.get(OperatingMode)
        HWError={0x00:"No Error",0x01:"Fatal Error"}.get(HWError)
        pass
    def on_ECHO(self,data):
        """"""
        pass

    def on_HW_ERROR(self,linenumber,filename):
        """"""
        pass

    def on_CMD_RSP(self,CommandOpCode,Status,ResponseData):
        """"""
        pass
        if self.debug:
            print( "CMF_RSP {0} {1} {2}".format(CMDS.get(CommandOpCode),STATUS.get(Status),ResponseData))

    def on_SETUP_COMPLETED(self):
        pass
    def on_SETUP_CONTINUE(self):
        pass


    def on_CONNECTED(self,AddressType,PeerAddress,ConnectionInterval, SlaveLatencyn,SupervisionTimeout,MasterClockAccuracy):
        """
        AddressType 1 Peer Address Type
        PeerAddress 6 Peer Device Address
        ConnectionInterval 2 Connection Interval setting (LSB/
        MSB)
        SlaveLatency 2 Slave latency setting (LSB/MSB)
        SupervisionTimeout 2 Supervision timeout period (LSB/
        MSB)
        MasterClockAccuracy 1 Master (peer device) clock accuracy


        AddressType
        0x01 Public address
        0x02 Random Static Address
        0x03 Random Private Address (Resolvable)
        0x04 Random Private Address (Un-resolvable)
        ConnectionInterval - Connection interval set in periods of 1.25 ms
        SlaveLatency 0..1000
        (0x0000 - 0x03E8)
        The number of consequtive connection events
        that the slave is not required to respond
        SupervisionTimeout - Supervision timeout in seconds when multiplied
        with 10 ms
        MasterClockAccuracy 0x00 500 ppm
        0x01 250 ppm
        0x02 150 ppm
        0x03 100 ppm
        0x04 75 ppm
        0x05 50 ppm
        0x06 30 ppm
        0x07 20 ppm
        """
        AddressType={0x01 :"Public address",
         0x02 :"Random Static Address",
         0x03 :"Random Private Address (Resolvable)",
         0x04 :"Random Private Address (Un-resolvable)"
        }.get(AddressType)
        if self.debug:
            print(AddressType,PeerAddress)
        

    def on_DISCONNECTED(self,AciStatus,BtLeStatus):
        """
        AciStatus 1 Reason for disconnection
        (Local Host origin)
        BtLeStatus 1 Reason for disconnection, Bluetooth
        error code
        (Origin not related to local Host)
        AciStatus 
        0x03 Check the Bluetooth low energy status code; 
        BtLeStatus
        0x93 Timeout while advertising, unable to establish connection
        0x94 Remote device failed to complete a Security Manager
        procedure1
        1. Also generated under Connect (No bonded relationship) state if Security Manager procedure
        was initiated by peer.
        """
        pass
        
    def on_BOND_STATUS(self,*args):
        """"
        BondStatusCode 1 Bond Status code
        BondStatusSource 1 Bond Status source
        BondStatus-SecMode1 1 LE security mode 1
        BondStatus-SecMode2 1 LE security mode 2
        BondStatus-KeyExchSlave 1 Keys exchanged (slave)
        BondStatus-KeyExchMaster 1 Keys exchanged (master)  

        BondStatusCode 
        0x00 Bond suceeded
        0x01..0xFF Bond Failed, see section 28.2 on page 159 for more
        information
        BondStatusSource 0x01 Status code generated locally
        0x02 Status code generated by the remote peer
        BondStatus-SecMode1 - Levels supported in LE Security Mode 1
        • bit0: level 1
        • bit1: level 2
        • bit2: level 3
        • bit3..7: reserved
        BondStatus-SecMode2 - Levels supported in LE Security Mode 2
        • bit0: level 1
        • bit1: level 2
        • bit2..7: reserved
        BondStatus-KeyExchSlave - Keys exchanged (slave distributed keys)
        • bit0: LTK using Encryption Information
        command
        • bit1: EDIV and Rand using Master Identification
        command
        • bit2: IRK using Identity Information command
        • bit3: Public device or static random address
        using Identity Address Information command
        • bit4: CSRK using Signing Information
        command
        • bit5..7: reserved
        BondStatus-KeyExchMaster - Keys exchanged (master distributed keys)
        • bit0: LTK using Encryption Information
        command
        • bit1: EDIV and Rand using Master Identification
        command
        • bit2: IRK using Identity Information command
        • bit3: Public device or static random address
        using Identity Address Information command
        • bit4: CSRK using Signing Information
        command
        • bit5..7: reserved      
        """
        pass

    def on_PIPE_STATUS(self,PipesOpen,PipesClosed):
        """
        PipesOpen - Bitmap where each of the bits 1 to 62 represents the service pipes with the
        number 1 to 62. Bit 63 is not in use.
        A "1" means that the corresponding pipe is open, while a "0" means that the
        pipe is unavailable.
        Bit 0 in the first byte contains the nRF8001 service discovery procedure
        execution status:
        • When set to 1, the nRF8001 initiated service discovery procedure has
        completed.
        • When set to 0, the nRF8001 initiated service discovery has not yet
        completed1.
        1. If service discovery is not required for nRF8001 (based on the existing service configuration), Bit 0 in the first bitmap
        byte is set to 1.
        
        PipesClosed - Bitmap where each of the bits 1 to 62 represents the service pipes with the
        number 1 to 62. Bit 63 is not in use.
        A "1" means that the corresponding pipe requires opening, while a "0"
        means that no action is required.
        Bit 0 in the first byte contains is always set to “0”
        """
        def toTable(bitmap):
            po=map("{0:0>8b}".format,bitmap)
            po=map(reversed,po)
            po=map("".join,po)
            po="".join(po)
            return po
        self.PipesOpen   = toTable(PipesOpen)
        self.PipesClosed = toTable(PipesClosed)
        #print("O",self.PipesClosed)
        #print("C",self.PipesClosed)

        #self.cmd_ChangeTimingRequest()
    
    def on_TIMING(self,*args):
        """
        Content
        ConnectionInterval 2 Connection interval for the actual
        connection (MSB first)
        SlaveLatency 2 Slave latency setting (LSB/MSB)
        SupervisionTimeout 2 Supervision timeout for the connection
        (multiple of 10 ms)

        ConnectionInterval 6..3200 Connection interval = data value multiplied by
        1,25 ms
        SlaveLatency 0..1000
        (0x0000 - 0x03E8)
        The number of consequtive connection events
        that the slave is not required to respond
        SupervisionTimeout 10..3200 Timeout = data value multiplied by 10 ms
        """
        pass
    
    def _on_DATA_CREDIT(self,DataCredits):
        """Internal """
        self.DataCreditAvailable+= DataCredits
        self.on_DATA_CREDIT(DataCredits)

    def on_DATA_CREDIT(self,DataCredits):
        """DeviceStartedEvent Data service pipes disconnected: No credits can be used
        PipeStatusEvent Data service pipes are connected and in open state: Credits can be used
        for the service pipes identified as open
        DisconnectedEvent Data pipes disconnected: No credits can be used
        DataAckEvent No effect on buffer memory status
        DataCreditEvent (n) Returns n buffer memory credits to the application controller
        DataReceivedEvent No effect on buffer memory status
        SendData Uses ONE available credit
        SendDataAck Uses ONE available credit
        SendDataNack Uses ONE available credit
        RequestData Uses ONE available credit
        OpenRemotePipe No effect on buffer memory status"""
        pass
           
    def on_DATA_ACK(self,ServicePipeNumber):
        "On doit acquiter"
        raise Exception("Not Implemented")
    
    def on_DATA_RECEIVED(self,ServicePipeNo,data):
        if self.debug:
            print("#{0}:{1}".format(ServicePipeNo,data))
    
    def on_PIPE_ERROR(self,ServicePipeNo,ErrorCode,ErrorData):
        ErrorText = STATUS.get(ErrorCode)
        if self.debug:
            print("on_PIPE_ERROR",ServicePipeNo,ErrorText,ErrorData)
        raise Exception("Pipe Error")

    def on_DISPLAY_PASSKEY(self,Passkey):
        """
        Passkey A fixed 6 byte ASCII string representing the passkey (no
        NULL termination, '0'-'9' digits only) The number has to be
        padded with zeroes if shorter than six digits.
        Examples: "000123", "999999", "000000"
        """
        raise Exception("Not Implemented")

    def on_KEY_REQUEST(self,KeyType):
        """KeyType 0x01 Passkey requested"""
        raise Exception("Not Implemented")
   
        
    def loop(self):
        while 1:
            time.sleep(0.1)
            event=self.peek_event()
            if event[0] != 0xFF:
                print(event)


# class PyBoardBt(NRF8001):
#     msgs=[
#        [ 0x07, 0x06, 0x00, 0x00, 0x03, 0x02, 0x42, 0x07 ],
#         [ 0x1F, 0x06, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x07, 0x01, 0x01, 0x00, 0x00, 0x06, 0x00, 0x00, 0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
#         [ 0x1F, 0x06, 0x10, 0x1C, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x03, 0x90, 0x01, 0xFF ],
#         [ 0x1F, 0x06, 0x10, 0x38, 0xFF, 0xFF, 0x02, 0x58, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
#         [ 0x05, 0x06, 0x10, 0x54, 0x00, 0x00 ],
#         [ 0x1F, 0x06, 0x20, 0x00, 0x04, 0x04, 0x02, 0x02, 0x00, 0x01, 0x28, 0x00, 0x01, 0x00, 0x18, 0x04, 0x04, 0x05, 0x05, 0x00, 0x02, 0x28, 0x03, 0x01, 0x0E, 0x03, 0x00, 0x00, 0x2A, 0x04, 0x14, 0x0A ],
#         [ 0x1F, 0x06, 0x20, 0x1C, 0x0A, 0x00, 0x03, 0x2A, 0x00, 0x01, 0x42, 0x4C, 0x45, 0x20, 0x53, 0x68, 0x69, 0x65, 0x6C, 0x64, 0x04, 0x04, 0x05, 0x05, 0x00, 0x04, 0x28, 0x03, 0x01, 0x02, 0x05, 0x00 ],
#         [ 0x1F, 0x06, 0x20, 0x38, 0x01, 0x2A, 0x06, 0x04, 0x03, 0x02, 0x00, 0x05, 0x2A, 0x01, 0x01, 0x00, 0x00, 0x04, 0x04, 0x05, 0x05, 0x00, 0x06, 0x28, 0x03, 0x01, 0x02, 0x07, 0x00, 0x04, 0x2A, 0x06 ],
#         [ 0x1F, 0x06, 0x20, 0x54, 0x04, 0x09, 0x08, 0x00, 0x07, 0x2A, 0x04, 0x01, 0x06, 0x00, 0x12, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x04, 0x04, 0x02, 0x02, 0x00, 0x08, 0x28, 0x00, 0x01, 0x01, 0x18, 0x04 ],
#         [ 0x1F, 0x06, 0x20, 0x70, 0x04, 0x05, 0x05, 0x00, 0x09, 0x28, 0x03, 0x01, 0x22, 0x0A, 0x00, 0x05, 0x2A, 0x26, 0x04, 0x05, 0x04, 0x00, 0x0A, 0x2A, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x46, 0x14 ],
#         [ 0x1F, 0x06, 0x20, 0x8C, 0x03, 0x02, 0x00, 0x0B, 0x29, 0x02, 0x01, 0x00, 0x00, 0x04, 0x04, 0x10, 0x10, 0x00, 0x0C, 0x28, 0x00, 0x01, 0x1E, 0x94, 0x8D, 0xF1, 0x48, 0x31, 0x94, 0xBA, 0x75, 0x4C ],
#         [ 0x1F, 0x06, 0x20, 0xA8, 0x3E, 0x50, 0x00, 0x00, 0x3D, 0x71, 0x04, 0x04, 0x13, 0x13, 0x00, 0x0D, 0x28, 0x03, 0x01, 0x04, 0x0E, 0x00, 0x1E, 0x94, 0x8D, 0xF1, 0x48, 0x31, 0x94, 0xBA, 0x75, 0x4C ],
#         [ 0x1F, 0x06, 0x20, 0xC4, 0x3E, 0x50, 0x03, 0x00, 0x3D, 0x71, 0x44, 0x10, 0x14, 0x00, 0x00, 0x0E, 0x00, 0x03, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
#         [ 0x1F, 0x06, 0x20, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x13, 0x13, 0x00, 0x0F, 0x28, 0x03, 0x01, 0x10, 0x10, 0x00, 0x1E, 0x94, 0x8D, 0xF1, 0x48, 0x31, 0x94, 0xBA, 0x75 ],
#         [ 0x1F, 0x06, 0x20, 0xFC, 0x4C, 0x3E, 0x50, 0x02, 0x00, 0x3D, 0x71, 0x14, 0x00, 0x14, 0x00, 0x00, 0x10, 0x00, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
#         [ 0x1F, 0x06, 0x21, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46, 0x14, 0x03, 0x02, 0x00, 0x11, 0x29, 0x02, 0x01, 0x00, 0x00, 0x04, 0x04, 0x02, 0x02, 0x00, 0x12, 0x28, 0x00, 0x01 ],
#         [ 0x1F, 0x06, 0x21, 0x34, 0x01, 0x00, 0x04, 0x04, 0x05, 0x05, 0x00, 0x13, 0x28, 0x03, 0x01, 0x0A, 0x14, 0x00, 0x02, 0x00, 0x44, 0x14, 0x01, 0x01, 0x00, 0x14, 0x00, 0x02, 0x01, 0x00, 0x04, 0x04 ],
#         [ 0x1F, 0x06, 0x21, 0x50, 0x14, 0x09, 0x00, 0x15, 0x29, 0x01, 0x01, 0x4C, 0x45, 0x44, 0x20, 0x56, 0x41, 0x4C, 0x55, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04 ],
#         [ 0x1F, 0x06, 0x21, 0x6C, 0x04, 0x05, 0x05, 0x00, 0x16, 0x28, 0x03, 0x01, 0x12, 0x17, 0x00, 0x03, 0x00, 0x16, 0x04, 0x04, 0x03, 0x00, 0x17, 0x00, 0x03, 0x01, 0x00, 0x00, 0x00, 0x46, 0x14, 0x03 ],
#         [ 0x1F, 0x06, 0x21, 0x88, 0x02, 0x00, 0x18, 0x29, 0x02, 0x01, 0x00, 0x00, 0x04, 0x04, 0x05, 0x05, 0x00, 0x19, 0x28, 0x03, 0x01, 0x12, 0x1A, 0x00, 0x04, 0x00, 0x16, 0x04, 0x02, 0x01, 0x00, 0x1A ],
#         [ 0x1F, 0x06, 0x21, 0xA4, 0x00, 0x04, 0x01, 0x00, 0x06, 0x04, 0x08, 0x07, 0x00, 0x1B, 0x29, 0x04, 0x01, 0x0C, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x46, 0x14, 0x03, 0x02, 0x00, 0x1C, 0x29, 0x02 ],
#         [ 0x07, 0x06, 0x21, 0xC0, 0x01, 0x00, 0x00, 0x00 ],
#         [ 0x1F, 0x06, 0x40, 0x00, 0x2A, 0x00, 0x01, 0x00, 0x80, 0x04, 0x00, 0x03, 0x00, 0x00, 0x2A, 0x05, 0x01, 0x00, 0x04, 0x04, 0x00, 0x0A, 0x00, 0x0B, 0x00, 0x03, 0x02, 0x00, 0x08, 0x04, 0x00, 0x0E ],
#         [ 0x1F, 0x06, 0x40, 0x1C, 0x00, 0x00, 0x00, 0x02, 0x02, 0x00, 0x02, 0x04, 0x00, 0x10, 0x00, 0x11, 0x00, 0x02, 0x01, 0x04, 0x00, 0x04, 0x00, 0x14, 0x00, 0x00, 0x00, 0x03, 0x01, 0x00, 0x02, 0x04 ],
#         [ 0x11, 0x06, 0x40, 0x38, 0x00, 0x17, 0x00, 0x18, 0x00, 0x04, 0x01, 0x00, 0x02, 0x04, 0x00, 0x1A, 0x00, 0x1C ],
#         [ 0x13, 0x06, 0x50, 0x00, 0x1E, 0x94, 0x8D, 0xF1, 0x48, 0x31, 0x94, 0xBA, 0x75, 0x4C, 0x3E, 0x50, 0x00, 0x00, 0x3D, 0x71 ],
#         [ 0x18, 0x06, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
#         [ 0x06, 0x06, 0xF0, 0x00, 0x03, 0x96, 0xBA ],
#         ]

#     def __init__(self, spi=SPI(1), req=Pin('X5'), rdy=Pin('X4'),act=None,rst=Pin('X3'),debug=True):
#         super(PyBoardBt,self).__init__(spi,req,rdy,act,rst,debug)
#         self.accel=machine.Accel()
#         self.rtc=machine.RTC()
        
#     def on_SETUP_COMPLETED(self):
#         print("SETUP COMPLETED !!")
    
#     def on_SETUP_CONTINUE(self):
#         pass
    
#     def on_DEVICE_STARTED(self,OperatingMode,HWError,DataCreditAvailable):
#         """ 
#             OperatingMode 1 Current device mode
#             HWError 1 Cause of the restart
#             DataCreditAvailable
#         """
#         OperatingModeText={0x01:"Test",0x02:"Setup",0x03:"Standby"}.get(OperatingMode)
#         HWError={0x00:"No Error",0x01:"Fatal Error"}.get(HWError)
#         print("DEVICE STARTED",OperatingModeText,HWError)
#         print("DATACREDIT",self.DataCreditAvailable)
#         #if OperatingModeText ==0x03:
#         #    self.cmd_connect()

#     def on_DISCONNECTED(self,AciStatus,BtLeStatus):
#         self.cmd_connect()
#     def on_DATA_RECEIVED(self,ServicePipeNo,data):

#         if ServicePipeNo==3:    #UART TX
#             print("TX",data)
#             if data==b'V':
#                 if self.PipesOpen[4]=="1":
#                     self.cmd_SendData(4,[b"V",0x00,0x00,0x01])
#             elif data==b'C':
#                 if self.PipesOpen[4]=="1":
#                     self.cmd_SendData(4,[0x00])
#             elif data==b'M':
#                 if self.PipesOpen[4]=="1":
#                     pass
#                     #self.cmd_SendData(4,[0x00,0x00,0x01])
#             elif data==b'S':
#                 if self.PipesOpen[4]=="1":
#                     pass
#                     #self.cmd_SendData(4,[0x00,0x00,0x01])

#             elif data==b"erase":
#                 lcd.fill(0)
#                 lcd.show()
#             elif data==b"qui est la":
#                 if self.PipesOpen[4]=="1":
#                     self.cmd_SendData(4,b'joachim')
#             elif lcd:
#                 lcd.write(data +"\n")
#         elif ServicePipeNo==5:#led Commande 
#             #print("LED",data)
#             values="{0:0>5b}".format(struct.unpack("B",data)[0] & 15)
#             print(values)
#             for i in range(1,5):
#                 if values[i]=="1":
#                     machine.LED(i).on()
#                 else:
#                     machine.LED(i).off()
#     def loop(self):
#         while 1:
#             time.sleep(200)

#             try:
#                 event=bt.peek_event()
#             except Exception as e:
#                 print("ERROR :",e)

#             print(event)

#             # if self.PipesOpen[6]=="1":
#             #     #acc
#             #     self.cmd_SendData(6,struct.pack("bbb",self.accel.x()+decal,self.accel.y()+decal,self.accel.z()+decal))

#             #     data='{3} {2:>02}{1:>02}{0} {4:>02}:{5:>02}:{6:>02}'.format(*dt[:-1])
#             #     lastdate=dt[:-1]
                
#             #     if self.PipesOpen[7]=="1":
#             #         self.cmd_SendData(7,data.encode())

def init():
    import machine
    print("initing NRF8001")
    # bt=NRF8001(SPI(0, 2_000_000), req=Pin(5), rdy=Pin(1), act=Pin(0), rst=Pin(6),debug=True)
    bt=NRF8001(SPI(0, 2_000_000), req=Pin(5), rdy=Pin(1), act=None, rst=Pin(6),debug=True)
    print("resetting NRF8001")

    bt.reset()

    print("testing")
    # bt._test()
    bt.setup(msgs)
    # print("DO ADVERTISING")
    bt.cmd_connect()
    bt.cmd_SetLocalData(3,b"end setup")
        
    bt.loop()


