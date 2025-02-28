import threading
import random
import time

class Validator(threading.Thread):

    def __init__(self, queue):
        super().__init__()
        self.queue_map = queue
        self.is_running = True
        self.std_for_temperature = 10
        self.std_for_pressure = 15
        self.std_for_voltage = 2
        
    def run(self):
        while(self.is_running):
            incoming_data = "t1," + str(round(max(30, min(random.normalvariate(70, self.std_for_temperature),  80)))) + ",v1," + str(round(max(0, min(random.normalvariate(2, self.std_for_voltage),  5)))) + ",t2," + str(round(max(30, min(random.normalvariate(50, self.std_for_temperature),  80)))) + ",v2," + str(round(max(0, min(random.normalvariate(2, self.std_for_voltage),  5)))) + ",t3," + str(round(max(30, min(random.normalvariate(50, self.std_for_temperature),  80))))+ ",v3," + str(round(max(0, min(random.normalvariate(2, self.std_for_voltage),  5)))) + ",t4," + str(round(max(30, min(random.normalvariate(50, self.std_for_temperature),  80)))) + ",v4," + str(round(max(0, min(random.normalvariate(2, self.std_for_voltage),  5)))) + ",p," + str(round(max(50, min(random.normalvariate(75, self.std_for_pressure),  110))))  
            self.validate_data(incoming_data)
            time.sleep(0.5)
        print("thread ended")

    def validate_data(self,data):
        data_split = data.split(',')
        sensor_data = []
        while len(data_split) > 0:
            sensor_id = data_split.pop(0)
            sensor_data = data_split.pop(0)
            if (sensor_id == "t1" or sensor_id == "t2" or sensor_id == "t3" or sensor_id == "t4"):   
                if(self.isfloat(sensor_data)):
                    self.queue_map[sensor_id].put((sensor_id,"temperature",sensor_data,"valid"))
                else:
                    self.queue_map[sensor_id].put((sensor_id,"temperature",sensor_data,"invalid"))
            if (sensor_id == "v1" or sensor_id == "v2" or sensor_id == "v3" or sensor_id == "v4"):    
                if(self.isfloat(sensor_data)):
                    self.queue_map[sensor_id].put((sensor_id,"voltage",sensor_data,"valid"))
                else:
                    self.queue_map[sensor_id].put((sensor_id,"voltage",sensor_data,"invalid"))
            else:
                if(self.isfloat(sensor_data)):
                    self.queue_map[sensor_id].put((sensor_id,"pressure",sensor_data,"valid"))
                else:
                    self.queue_map[sensor_id].put((sensor_id,"pressure",sensor_data,"invalid")) 
    
    def isfloat(self,string):
        try:
            float(string)
            return True
        except ValueError:
            return False
        
    def end_thread(self):
        self.is_running = False     