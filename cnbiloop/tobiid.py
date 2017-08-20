
SetOnly = 0
GetOnly = 1
SetGet  = 2

class TobiId:

    def __init__(self, mode):
        self._address = ""
        self._port    = ""
        self._mode    = mode

    def Attach(self, address, port):
        self._address = address
        self._port    = port

    def Dump(self):
        print "Store address::port: %s::%s" % (self._address, self._port)

