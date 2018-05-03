#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

def getDataServer(sock):
    data = sock.recv(1024)
    #print data
    return data

def ConnectServer():
    sock = socket.socket()
    sock.connect(('192.168.0.84', 8599))
    return sock

def DisconectServer(sock):
    sock.close()