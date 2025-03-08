import threading
import time 
import numpy as np
import matplotlib
from Notifications import Notifications
from datetime import datetime
matplotlib.use('TkAgg')
import csv


class Monitor_thread(threading.Thread):
    
    def __init__(self, input_queue, graph_queue, notification_queue, datatype, datatype_max, datatype_min, monitor_id, configuration, timer=0.5, safety_state=None, value_state="safe"):
        super().__init__()
        self.queue = input_queue
        self.monitor_id = monitor_id
        self.monitor_values = []
        self.error_values = []
        self.sensor_datatype = datatype
        self.datatype_max = datatype_max
        self.datatype_min = datatype_min
        self.datatype = datatype
        self.monitor_counter = 0
        self.value_state = value_state
        self.safety_state = safety_state
        self.last_error_type = None
        self.current_error_type = None
        self.error_counter = 0
        self.ejection_timer = None
        self.graph_queue = graph_queue 
        self.is_running = True
        self.safe_flag = True
        self.notification_queue = notification_queue
        self.ejection_timer_notification_counter = 0
        self.timer = timer
        self.notification = ""
        self.configuration = configuration
        
    def run(self):
        while(self.is_running == True):
            if not self.queue.empty():
                self.value_analysis()        
            time.sleep(self.timer)
            
    def value_analysis(self):
        sensor_data = self.queue.get()
        monitor_length = self.configuration.get_monitor_length()
        error_length = self.configuration.get_error_length()
        value = float(sensor_data[2])
        if self.safety_state == "eject":
            # No longer need to monitor sensor
            self.end_thread()
            pass
        
        #maintains the monitor value length of 1000 and removes old monitor values from the error values list
        if(len(self.monitor_values) > monitor_length - 1):
            value_to_be_removed = self.monitor_values.pop(0)
            if(value_to_be_removed in self.error_values):
                self.error_values.remove(value_to_be_removed)
                self.error_counter = self.error_counter - 1
        #declares the battery being monitored in a safe state and turns mosfet back on once its been done doesnt have to occur again which is what the flag represents
        if (self.value_state == "safe" and self.safe_flag == False):
            self.safe_flag = True
            # turn off mosfet
            self.notification = self.monitor_id +" mostfet turned off : Time = " + datetime.now().isoformat()
            self.notification_queue.put(Notifications(self.notification, "mosfet"))
            self.safety_state = None
            self.add_notification()
            self.update_sensor_states()
        #safe value path
        if ((self.datatype_min <= value and value <= self.datatype_max ) and sensor_data[3] != "invalid"):
            self.monitor_values.append(value)
            self.graph_queue.put(value)
            if (self.monitor_counter < monitor_length):
                self.monitor_counter  = self.monitor_counter + 1
            if (self.monitor_counter == monitor_length):
                self.value_state = "safe"
                self.update_sensor_states()
    
        #unsafe value path               
        else:
            # maintains a list size of 200 for errors by removing oldest error value
            if (len(self.error_values) > error_length - 1):
                self.error_values.pop(0)
            # if value recieved from mc is invalid
            if sensor_data[3] == "invalid":
                self.monitor_values.append(np.nan)
                self.error_values.append((value,"invalid"))
                self.graph_queue.put(np.nan)
                self.current_error_type = "invalid"
            # if value recieved from mc is below safe conditions
            elif value < self.datatype_min:
                self.error_values.append((value,"under"))
                self.monitor_values.append(value)
                self.current_error_type = "under"
                self.graph_queue.put(value)
            # if value recieved from mc is over safe conditions    
            else:
                self.error_values.append((value,"over"))
                self.monitor_values.append(value)
                self.current_error_type = "over"
                self.graph_queue.put(value)
            self.monitor_counter = 0
            self.value_state = "unsafe"
            self.update_sensor_states()
            self.safe_flag = False
            self.error_check()

    def error_check(self):
        ejection_time = self.configuration.get_ejection_time()
        if( len(self.error_values) > 0):
            # if the error counter for the error type is over 80% of the errors occured Note I might want to have a counter for each error type in the cause of a sensor malfunction where several errors are constantly thrown
            if float(self.error_counter / len(self.error_values)) >= 0.80 and  len(self.error_values) > 180:    
                if self.safety_state == None:
                    if (self.current_error_type == "invalid"):
                        self.value_state = "unsafe"
                        self.update_sensor_states()
                    else:
                        self.safety_state = "mosfet"
                        # turn on mosfet
                        self.notification = self.monitor_id +" mosfet triggered : Time = " + datetime.now().isoformat()
                        self.notification_queue.put(Notifications(self.notification, "mosfet"))
                        self.ejection_timer = time.time()
                        self.ejection_timer_notification_counter = 0 
                        self.add_notification()
                        self.update_sensor_states()     
                if self.safety_state == "mosfet":
                    if ((time.time() - self.ejection_timer) < ejection_time):
                        self.ejection_timer_notification_counter = self.ejection_timer_notification_counter + 1
                        if(self.ejection_timer_notification_counter == 120):
                        #notify UI with the time spend in the error state
                            self.notification = self.monitor_id + " ejection will commence in " + str(self.ejection_time - (time.time() - self.ejection_timer)) + " : Time = " + datetime.now().isoformat()
                            self.notification_queue.put(Notifications(self.notification,"ejection"))
                            self.ejection_timer_notification_counter = 0
                            self.add_notification()
                    if ((time.time() - self.ejection_timer) >= ejection_time):
                        #eject
                        self.notification = self.monitor_id +" eject triggered : Time = " + datetime.now().isoformat()
                        self.notification_queue.put(Notifications(self.notification, "ejection"))
                        # only if we eject set state to eject
                        self.safety_state = "eject"
                        self.add_notification()
                        self.update_sensor_states()
            else:
                if self.last_error_type == None:
                    self.last_error_type = self.current_error_type
                if self.last_error_type == self.current_error_type:
                    self.error_counter = self.error_counter + 1
                elif self.last_error_type == "over" and self.current_error_type == "under" or self.last_error_type == "under" and self.current_error_type == "over":
                    self.error_counter = self.error_counter + 1
                else:
                    self.error_counter = 0 
                    self.last_error_type = self.current_error_type                   
    
    def end_thread(self):
        self.is_running = False

    def update_sensor_states(self):
        data = {"safety_state" : self.safety_state,
                "value_state" : self.value_state}
        file_path = str(self.monitor_id + ".csv")
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            row = list(csv_reader)
            header = csv_reader.fieldnames
        if row:
            row[0].update(data)
        with open(file_path, mode="w",newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=header)
            csv_writer.writeheader()
            csv_writer.writerows(row)

    def add_notification(self):
        current_time = datetime.now().isoformat()

        with open("notification_log.csv", mode="a", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([self.monitor_id,self.notification,current_time])



