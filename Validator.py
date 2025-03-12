import threading
import random
import time
import numpy as np

class Validator(threading.Thread):

    def __init__(self, queue):
        super().__init__()
        self.queue_map = queue
        self.is_running = True
        self.noise_level_temperature = 0.5
        self.noise_level_pressure = 0.75
        self.noise_level_voltage = 0.75
        self.initial_temp_1 = 40
        self.initial_temp_2 = 40
        self.initial_temp_3 = 40
        self.initial_temp_4 = 40
        self.initial_volt1 = 2
        self.initial_volt2 = 2
        self.initial_volt3 = 2
        self.initial_volt4 = 2
        self.initial_pressure = 70
    
    def run(self):
        while(self.is_running):
            incoming_data = "t1," + str(self.random_walk(self.initial_temp_1,self.noise_level_temperature))   + ",v1," + str(self.random_walk_volt(self.initial_volt1,self.noise_level_voltage)) + ",t2," + str(self.random_walk(self.initial_temp_2,self.noise_level_temperature)) + ",v2," + str(self.random_walk_volt(self.initial_volt2,self.noise_level_voltage)) + ",t3," + str(self.random_walk(self.initial_temp_3,self.noise_level_temperature)) + ",v3," + str(self.random_walk_volt(self.initial_volt3,self.noise_level_voltage)) + ",t4," + str(self.random_walk(self.initial_temp_4,self.noise_level_temperature)) + ",v4," + str(self.random_walk_volt(self.initial_volt4,self.noise_level_voltage)) + ",p," + str(self.random_walk(self.initial_pressure,self.noise_level_pressure))  
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
        
    def random_walk(self, current_value, noise_level):
        step = np.random.normal(0, noise_level)
        current_value += step
        return current_value
    
    def random_walk_volt(self, current_value, noise_level):
        step = np.random.normal(0,noise_level)
        if (current_value >= 4):
            if (step > 0):
                chance = np.random.randint(0,100)
                if (chance > 70):
                    current_value += step
            else:
                current_value += step            
        elif (current_value <= 0):
            if (step < 0):
                chance = np.random.randint(0,100)
                if (chance > 70):
                    current_value += step
            else:
                current_value += step
        else:
            current_value += step
        return current_value
        