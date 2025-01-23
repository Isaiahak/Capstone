import socket
import threading

batteries = {"battery 1" : {"temperature" : [], "voltage": []},
            "battery 2" : {"temperature" : [], "voltage": []},
            "battery 3" : {"temperature" : [], "voltage": []},
            "battery 4" : {"temperature" : [], "voltage": []}}

pressures = []
batteryQueue = []
pressureQueue = []

safe_temperature_value = 70 # +/- 10% gives you within safe operating temperatures of slightly over 
dangerous_temperature_value = None #figure out
previous_temperature_value = None 

safe_voltage_value = 3.34 # +/- 10% gives you full charge or under
dangerous_voltage_value = None #figure out
previous_voltage_value = None


safe_pressure_value = None #figure out
dangerous_pressure_value = None #figure out
previous_pressure_value = None
        
    

def validateData(battery,dataType,data):
    if dataType == "temperature":
        #check if the temperature is within reasonable values including exceeding safe levels
        if data > safe_temperature_value:
            # i need to check how much above the safe temperature we are,
            pass
        if data <= safe_temperature_value:
            pass
        previous_temperature_value = data
        
    if dataType == "voltage":
        # check if the voltage is wthin reasonable values incklduign exceeding safe levels
        if data > safe_voltage_value:
            pass
        if data <= safe_voltage_value:
            pass
        previous_voltage_value = data
    batteries[battery][dataType].append(data)
    batteryQueue.append("battery,dataType,data")
    # check the data received from the connector to see if its a value int or not then add to a queue to averaging

def validatePressureData(dataType,data):
    if dataType =='pressure':
        if data > safe_pressure_value:
            pass
        if data <= safe_pressure_value:
            pass
        previous_voltage_value = data
    pressures.append(data)
    pressureQueue.append(data)
    
def sendAlertMessage(battery,dataType,data):
    # send an alert mesage to be displayed on the UI depending on the sensor value readings
    pass

def monitoringProcess(self):
    # process of monitoring values
    pass

def recieveData(battery,dataType,data): 
    validateData()
    monitoringProcess()
    pass 

def recievePressureData(self,dataType,data):
    validatePressureData()
    monitoringProcess()
    pass
        
def fetch_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8000))
    data = s.recv(1024).decode()
    split_data = data.split(",")
    
    if split_data[0] == "p":
        split_data.pop(0)
        recievePressureData("pressure",split_data[0])
    else:
        battery_number = split_data.pop(0)
        recieveData("battery " + battery_number, "temperature", split_data.pop(0))
        recieveData("battery " + battery_number, "voltage", split_data.pop(0))   
    s.close()
    
def send_data():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.bind(('localhost', 8001))  # Connect to another server
    send_socket.listen()
    while True:
        if not batteryQueue or not pressureQueue: 
            if not batteryQueue:   
                # Get input from the user or your program
                print(batteryQueue[0])
                send_socket.sendall(batteryQueue.pop(0).encode())  # Send the data to the connected server            
            if not pressureQueue:
                print(batteryQueue[0])
                send_socket.sendall(pressureQueue.pop(0).encode())
        send_socket.close()
          
def start_server():
    # Start the listen_for_data function in a separate thread
    reciever_thread = threading.Thread(target=fetch_data)
    reciever_thread.start()
    # Start the send_data function in a separate thread
    sender_thread = threading.Thread(target=send_data)
    sender_thread.start()
    # Wait for both threads to finish (although they'll run indefinitely)
    reciever_thread.join()
    sender_thread.join()

