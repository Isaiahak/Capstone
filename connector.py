class connector:

    batteries = {"battery 1" : {"temperature" : [], "voltage": []},
                 "battery 2" : {"temperature" : [], "voltage": []},
                 "battery 3" : {"temperature" : [], "voltage": []},
                 "battery 4" : {"temperature" : [], "voltage": []}}
    
    pressure = []

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        #asd

    def startup(self):
        #used to create the connection to the microcontroller 
    
    def recieveData(self):
        # recieve data from the micro controller 

    def passToMonitor(self):
        # pass the data and its id to thw sensor for it be to queued

    def toggleMOSFET(self):
        # used to tell the microcontroller which mosfet to switch on/off
    
    def resetEjection(self):
        # reset the ejection mechanism to its default location

    def Eject(self):
        # tells the ejection mechanism where to move 

    
    