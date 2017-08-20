import socket
import sys
from cnbicore import NetworkTypes

class Client:
    def __init__(self):
        self.__sock      = None
        self.__protocol  = None
        self.__address   = None
        self.__connected = False

    
