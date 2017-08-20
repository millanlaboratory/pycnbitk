import socket
import sys
from cnbicore import NetworkTypes

class Client:

    def __init__(self):
        self.__sock      = None
        self.__protocol  = None
        self.__address   = None
        self.__connected = False
        

    def Connect(self, address, port, protocol = NetworkTypes.SOCKET_PROTOCOL_TCP):
        
        if self.__sock:
            return NetworkTypes.SOCKET_ERROR_BOUND
        
        self.__address  = (address, int(port))
        self.__protocol = protocol
        
        if self.__protocol == NetworkTypes.SOCKET_PROTOCOL_TCP:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.__protocol == NetworkTypes.SOCKET_PROTOCOL_UDP:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            return NetworkTypes.SOCKET_ERROR_PROTOCOL
       
        try:
            self.__sock.connect(self.__address)
        except socket.error:
            self.Disconnect()
            return NetworkTypes.SOCKET_ERROR_CONNECTION

        self.__connected = True
        return NetworkTypes.SOCKET_SUCCESSFULL

    def Disconnect(self):
        if self.__connected == False:
            return True

        self.__sock.close()
        self.__sock = None

    def IsConnected(self):
        return self.__connected

    def Send(self, message):
        if self.__connected == False:
            return SOCKET_ERROR_CONNECTION

        self.__sock.sendall(message)
