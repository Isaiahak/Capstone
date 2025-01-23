import time
import random
import socket


pressure = []
instance = None
batteries = {"battery 1" : {"temperature" : [], "voltage": []},
                "battery 2" : {"temperature" : [], "voltage": []},
                "battery 3" : {"temperature" : [], "voltage": []},
                "battery 4" : {"temperature" : [], "voltage": []}}   

def parseData(data):
    data_split = data.split(',')
    sensor_data = []
    while len(data_split) > 1:
        battery_number = data_split.pop(0)
        battery_temperature = data_split.pop(0)
        battery_voltage = data_split.pop(0)
        sensor_data.append("battery " + battery_number + ", temperature, " + battery_temperature)
        sensor_data.append("battery " + battery_number, ", voltage, " + battery_voltage)
    sensor_data.append("pressure ," + data_split.pop())
    return sensor_data


def toggleMOSFET():
    # used to tell the microcontroller which mosfet to switch on/off
    pass

def resetEjection():
    # reset the ejection mechanism to its default location
    pass

def Eject():
    # tells the ejection mechanism where to move 
    pass

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen()
    print("Server is listening on port 8000...")
    while True:
        client_socket, address = server_socket.accept()
        #for now we are not getting the values from the micro controller but i should in the future
        incoming_data = "1," + str(random.randint(30,70)) + "," + str(random.randint(0,3)) + ", " 
        + "2," + str(random.randint(30,70)) + "," + str(random.randint(0,3)) + ", "
        + "3," + str(random.randint(30,70))+ "," + str(random.randint(0,3)) + ", "
        + "4," + str(random.randint(30,70)) + "," + str(random.randint(0,3)) + ", "
        + "p," + str(random.randint(50,100))
        parsed_data = parseData(incoming_data)
        for data in parsed_data:
            client_socket.send(data.encode())
        #client_socket.close()


