#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import socket
import sys

class Client:

    def __init__(self):
        self.__address   = None
        self.__connected = False

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setblocking(0) 

    def Connect(self, address, port):
        
        self.__address  = (address, int(port))
              
        try:
            self.__sock.connect(self.__address)
        except socket.error:
            return False 

        self.__connected = True
        return True

    def Disconnect(self):
        if not self.__connected:
            return True

        self.__sock.close()
        self.__connected = False
        self.__sock = None

    def IsConnected(self):
        return self.__connected

    def Send(self, message):
        if not self.__connected:
            return False

        try:
            self.__sock.sendall(message)
        except socket.error:
            self.__connected == False
            return False

    def Recv(self):
        if not self.__connected:
            return None
       
        msg = None
        try:
            msg = self.__sock.recv(512)
            if len(msg) == 0:
                self.__connected = False
                print "[client] - Broken pipe. Disconnection"
        except socket.error:
            msg = None
        
        return msg


if __name__ == '__main__': 
    import sys
    from time import sleep
    IP = "127.0.0.1"
    PORT = 8000
    client = Client()
    
    print "Try to connect to %s:%s" % (IP, PORT)
    while client.IsConnected() == False:
        client.Connect(IP, PORT)
    
    print "Connected to %s:%s" % (IP, PORT)

    FirstMessage = 100
    client.Send(str(FirstMessage))
    
    while client.IsConnected():
        sleep(1)
        data = client.Recv()

        if data:
            print "Received message: %s. " % (data)
            client.Send(str(int(data)+1))


    client.Disconnect()

