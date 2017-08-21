#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import socket
import sys

class Server:
    def __init__(self):
        self.__address   = None
        self.__connected = False
        self.__endpoint  = None
        self.__endpoint_address = None
        
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setblocking(0) 

    def Bind(self, address, port):

        self.__address  = (address, int(port))
             
        try:
            self.__sock.bind((address, int(port)))
            self.__sock.listen(0)
        except socket.error:
            return False
            
        return True

    def Accept(self, blocking = 0.0):
        
        while (blocking > 0.0 and self.IsConnected() == False):
            sleep(blocking)
            try:
                (self.__endpoint, self.__endpoint_address) = self.__sock.accept()
                self.__connected = True
                print "[server] - Enpoint connected from %s:%s" % \
                (self.__endpoint_address[0], self.__endpoint_address[1])
                
            except socket.error:
                self.__connected = False

        return True

    def GetEndpoint(self):
        if not self.__connected:
            return None
        else:
            return self.__endpoint_address

    def Disconnect(self):
        if not self.__connected:
            return True

        self.__endpoint.shutdown(2)
        self.__endpoint.close()
        self.__endpoint = None
        self.__connected = False
        self.__sock.shutdown(2)
        self.__sock.close()
        self.__sock = None
    
    def IsConnected(self):
        return self.__connected
    
    def Send(self, message):
        if not self.__connected:
            return False 
        
        try:
            self.__endpoint.sendall(message)
        except socket.error:
            self.__connected = False
            return False

        return True

    def Recv(self):
        if not self.__connected:
            return None

        broken = False
        try:
            msg = self.__endpoint.recv(512)
            if len(msg) == 0:
                broken = True
        except socket.error:
                broken = True
            
        if broken:
            self.__connected = False
            print "[server] - Broken pipe. Enpoint disconnected"
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

    server.Accept(1.0)
    
    while True:
        server.Accept(1.0)
        
        data = server.Recv()
        if data:
            print "Received message: %s" % (data)
            server.Send(data)
        sleep(1)

    server.Disconnect()
   
