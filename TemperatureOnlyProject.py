import queue
import tkinter as tk
from TemperatureOnlyUI import UI
from TemperatureOnlyValidator import Validator
from Monitoring_Threads import Monitor_thread
import csv
from Configuration import Configuration

#-------------------------------------------------Global-Variables---------------------------------------------------------------------------#
battery_1_temp_queue = queue.Queue()
battery_2_temp_queue = queue.Queue()
battery_3_temp_queue = queue.Queue()
battery_4_temp_queue = queue.Queue()

temp1_graph_queue = queue.Queue()
temp2_graph_queue = queue.Queue()
temp3_graph_queue = queue.Queue()
temp4_graph_queue = queue.Queue()

notification_queue = queue.Queue()

queue_map = {"t1" : battery_1_temp_queue, "t2" : battery_2_temp_queue, "t3" : battery_3_temp_queue, "t4" : battery_4_temp_queue} 

configuration = Configuration(monitor_length=1000, error_length=200, ejection_time=600, consistent_length=200, temp_diff=2, timer=0.5)
#-----------------------------------------------#application setup#-----------------------------------------------------------#      
def read_sensor_info(file_path):
        sensor_info = [None,None,None]
        with open(file_path, mode="r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                sensor_info[0] = row["safety_state"]
                sensor_info[1] = row["value_state"]
            return sensor_info
        
def on_closing():    
    b1_temp_thread.end_thread()
    b2_temp_thread.end_thread()
    b3_temp_thread.end_thread()
    b4_temp_thread.end_thread()
    validator_thread.end_thread()

    app.end_process()
    root.quit()
    root.destroy()
        
if __name__ == "__main__":

    temp1_values  = read_sensor_info("application_data/temp1.csv")
    b1_temp_thread = Monitor_thread(battery_1_temp_queue, temp1_graph_queue, notification_queue, "temperature", 60,30, "temp1",  configuration,  safety_state=temp1_values[1],value_state=temp1_values[2])
    b1_temp_thread.start()   
    print("b1 temp thread started")
    temp2_values  = read_sensor_info("application_data/temp2.csv")
    b2_temp_thread = Monitor_thread(battery_2_temp_queue, temp2_graph_queue, notification_queue,  "temperature", 60,30, "temp2",  configuration,  safety_state=temp2_values[1],value_state=temp2_values[2])
    b2_temp_thread.start()
    print("b2 temp thread started")
    temp3_values  = read_sensor_info("application_data/temp3.csv")
    b3_temp_thread = Monitor_thread(battery_3_temp_queue, temp3_graph_queue, notification_queue, "temperature", 60,30, "temp3", configuration,  safety_state=temp3_values[1],value_state=temp3_values[2])
    b3_temp_thread.start()
    print("b4 temp thread started")
    temp4_values  = read_sensor_info("application_data/temp4.csv")
    b4_temp_thread = Monitor_thread(battery_4_temp_queue, temp4_graph_queue, notification_queue, "temperature", 60,30, "temp4", configuration,  safety_state=temp4_values[1],value_state=temp4_values[2])
    b4_temp_thread.start()
    print("b4 temp thread started")

    validator_thread = Validator(queue_map)
    validator_thread.start()
    print("validator thread started")
    root = tk.Tk()
    root.title("Battery Monitor")
    root.geometry("1400x1000")  
    root.resizable(True, True) 
    app = UI(root,temp1_graph_queue, temp2_graph_queue, temp3_graph_queue, temp4_graph_queue, notification_queue, configuration)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    print("started GUI")
    root.mainloop()
    
