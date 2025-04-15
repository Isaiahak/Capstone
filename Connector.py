'''
import serial


class Connector:
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(Connector,cls).__new__(cls)
            return cls.instance
    

    def __init__(self):
        self.ser = serial.Serial(port = 'COM3', baudrate=9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)

    def recieve_data(self):
       


    def set_mosfet(self, state, battery_id):
        pass

    def eject_battery(self, battery_id):    
        pass

'''