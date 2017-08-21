#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import cnbicore.Client as client

class TobiId:

    SetOnly = 0
    GetOnly = 1
    SetGet  = 2

    def __init__(self, mode):
        self.__address = ""
        self.__port    = ""
        self.__mode    = mode
        self.__client = client.Client()

    def Attach(self, address, port):
        self.__address = address
        self.__port    = port
        return self.__client.Connect(address, port)

    def Detach(self):
        self.__address = ""
        self.__port    = ""
        self.__client.Disconnect()

    def IsAttached(self):
        return self.__client.IsConnected()

    



if __name__ == '__main__': 
    import sys
    from time import sleep

    IP   = '127.0.0.1'
    PORT = 8000

    tid = TobiId(TobiId.SetOnly)

    while not tid.IsAttached(): 
       tid.Attach(IP, PORT)

    print "TiD attached at %s:%s" % (IP, PORT)



