#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import socket
import sys
import NetworkTypes
import select
class Server:
    def __init__(self, protocol = NetworkTypes.SOCKET_PROTOCOL_TCP):
        self.__address   = None
        self.__connected = False
        self.__endpoint  = None
        self.__endpoint_address = None
        
        self.__protocol = protocol
        if self.__protocol == NetworkTypes.SOCKET_PROTOCOL_TCP:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.__protocol == NetworkTypes.SOCKET_PROTOCOL_UDP:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            return NetworkTypes.SOCKET_ERROR_PROTOCOL

        self.__sock.setblocking(0) 

    def Bind(self, address, port):

        self.__address  = (address, int(port))
             
        try:
            self.__sock.bind((address, int(port)))
            self.__sock.listen(0)
        except socket.error:
            return False
            
        return True

    def Accept(self):
        try:
            (self.__endpoint, addr) = self.__sock.accept()
            self.__connected = True
            self.__endpoint_address = addr
        except socket.error:
            return False

        return True
  
    def GetEndpoint(self):
        return self.__endpoint_address

    def Disconnect(self):
        if self.__connected == False:
            return True

        self.__endpoint.close()
        self.__endpoint = None
        self.__connected = False
        self.__sock.close()
        self.__sock = None
    
    def IsConnected(self):
        return self.__connected
    
    def Send(self, message):
        if self.__connected == False:
            return SOCKET_ERROR_CONNECTION

        self.__endpoint.sendall(message)

    def Recv(self):
        msg = None
        readable = select.select([self.__endpoint],[], [],0.0) 
       
        if readable:
            msg = self.__endpoint.recv(512)
            if len(msg) == 0:
                print "endpoint disconnected"
                return None
            else:   
                return msg


if __name__ == '__main__': 
    import sys
    from time import sleep
    IP = "127.0.0.1"
    PORT = 8000
    server = Server()
   

    if server.Bind(IP, PORT):
        print "Wait for connection at %s:%s" % (IP, PORT)
    else:
        print "Cannot bind at %s:%s" % (IP, PORT)

    while not server.Accept():
        sleep(1)

    endpoint = server.GetEndpoint()
    print "Endpoint connected from %s:%s" % (endpoint[0], endpoint[1])

    while True:
        #if not server.IsConnected():
        #    print "Endpoint disconnected"
        #    server.Accept()
        
        data = server.Recv()
        if data:
            print "Message: %s" % (data)

    server.Disconnect()
   
