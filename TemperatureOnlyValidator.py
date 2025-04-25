import threading
import random
import time
import numpy as np
from enum import Enum

class Value(Enum):
    RANDOM = 1
    SLOW_INCREMENT = 2
    SLOW_DECREMENT = 3

class Validator(threading.Thread):

    def __init__(self, queue):
        super().__init__()
        self.queue_map = queue
        self.is_running = True
        self.noise_level_temperature = 0.5
        self.initial_temp_1 = 40
        self.initial_temp_2 = 40
        self.initial_temp_3 = 40
        self.initial_temp_4 = 40
        self.increment_mode_1 = Value.RANDOM
        self.increment_mode_2 = Value.RANDOM
        self.increment_mode_3 = Value.RANDOM
        self.increment_mode_4 = Value.RANDOM
        self.increment_mode_map = {"t1": self.increment_mode_1,"t2": self.increment_mode_2,"t3": self.increment_mode_3,"t4": self.increment_mode_4}
        self.increment_counter = {"t1": 0,"t2": 0,"t3": 0,"t4": 0}
        self.decrement_counter = {"t1": 0,"t2": 0,"t3": 0,"t4": 0}
    
    def run(self):
        while(self.is_running):
            self.initial_temp_1 = self.update_value(self.initial_temp_1, self.increment_mode_1, "t1")
            self.initial_temp_2 = self.update_value(self.initial_temp_2, self.increment_mode_2, "t2")
            self.initial_temp_3 = self.update_value(self.initial_temp_3, self.increment_mode_3, "t3")
            self.initial_temp_4 = self.update_value(self.initial_temp_4, self.increment_mode_4, "t4")
            incoming_data = "t1," + str(self.initial_temp_1)   + ",t2," + str(self.initial_temp_2) + ",t3," + str(self.initial_temp_3) + ",t4," + str(self.initial_temp_4)   
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
        
    def update_value(self, current_value, current_mode, id):
        match current_mode:
            case Value.RANDOM:
                current_value = self.random_walk(current_value)
                if np.random.random() < 0.001:
                    self.increment_mode_map[id] = Value.SLOW_INCREMENT
                    self.increment_counter[id] = 0
                    print("increment")
            case Value.SLOW_INCREMENT:
                current_value = self.slow_increment(current_value,id)
                if self.increment_counter[id] >= 20000:
                    if np.random.random() < 0.8:
                        self.increment_mode_map[id] = Value.SLOW_DECREMENT
                        self.decrement_counter[id] = 0
                        print("decrement")
                    else:
                        self.increment_mode_map[id] = Value.RANDOM
                        print("random")
            case Value.SLOW_DECREMENT:
                current_value = self.slow_decrement(current_value,id)
                if self.decrement_counter[id] >= 10000:
                    self.increment_mode_map[id] = Value.RANDOM
                    print("random")
            case DEFAULT:
                current_mode = Value.RANDOM
        return current_value

    def random_walk(self, current_value):
        step = np.random.normal(0, self.noise_level_temperature)
        current_value += step
        return current_value
           
    def slow_increment(self, current_value, id):
        if (self.increment_counter[id] < 20000):
            current_value +=  0.001
            self.increment_counter[id] += 1
        else:
            self.increment_mode_map[id] = Value.RANDOM 
            self.increment_counter[id] = 0
        return current_value
    
    def slow_decrement(self, current_value, id):
        if (self.decrement_counter[id] < 10000):
            current_value -= 0.001
            self.decrement_counter[id] += 1
        else:
            self.increment_mode_map[id] = Value.RANDOM
            self.decrement_counter[id] = 0
        return current_value
 
        