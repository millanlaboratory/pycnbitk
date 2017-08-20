#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import socket
import sys
import NetworkTypes

class Client:

    def __init__(self, protocol = NetworkTypes.SOCKET_PROTOCOL_TCP):
        self.__address   = None
        self.__connected = False

        self.__protocol = protocol
        if self.__protocol == NetworkTypes.SOCKET_PROTOCOL_TCP:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.__protocol == NetworkTypes.SOCKET_PROTOCOL_UDP:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            return NetworkTypes.SOCKET_ERROR_PROTOCOL


    def Connect(self, address, port):
        
        self.__address  = (address, int(port))
              
        try:
            self.__sock.connect(self.__address)
        except socket.error:
            self.Disconnect()
            return NetworkTypes.SOCKET_ERROR_CONNECTION

        self.__connected = True
        return NetworkTypes.SOCKET_SUCCESSFUL

    def Disconnect(self):
        if self.__connected == False:
            return True

        self.__sock.shutdown(2)
        self.__sock.close()
        self.__connected = False
        self.__sock = None

    def IsConnected(self):
        return self.__connected

    def Send(self, message):
        if self.__connected == False:
            return SOCKET_ERROR_CONNECTION

        self.__sock.sendall(message)



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

    sleep(5)
    i = 0
    while i<5:
        client.Send('100')
        sleep(1)
        i = i+1

    client.Disconnect()

