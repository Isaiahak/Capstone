import queue
import tkinter as tk
from UI import UI
from Validator import Validator
from Monitoring_Threads import Monitor_thread
import csv

#-------------------------------------------------Global-Variables---------------------------------------------------------------------------#
battery_1_volt_queue = queue.Queue()
battery_1_temp_queue = queue.Queue()
battery_2_volt_queue = queue.Queue()
battery_2_temp_queue = queue.Queue()
battery_3_temp_queue = queue.Queue()
battery_3_volt_queue = queue.Queue()
battery_4_temp_queue = queue.Queue()
battery_4_volt_queue = queue.Queue()
temp1_graph_queue = queue.Queue()
temp2_graph_queue = queue.Queue()
temp3_graph_queue = queue.Queue()
temp4_graph_queue = queue.Queue()
volt1_graph_queue = queue.Queue()
volt2_graph_queue = queue.Queue()
volt3_graph_queue = queue.Queue()
volt4_graph_queue = queue.Queue()
pressure_graph_queue = queue.Queue()
pressure_queue = queue.Queue()
notification_queue = queue.Queue()

queue_map = {"v1" : battery_1_volt_queue,"v2" : battery_2_volt_queue, "v3" : battery_3_volt_queue, "v4" : battery_4_volt_queue,
             "t1" : battery_1_temp_queue, "t2" : battery_2_temp_queue, "t3" : battery_3_temp_queue, "t4" : battery_4_temp_queue,
             "p" : pressure_queue} 

ejection_time = 600
monitor_length = 1000
error_length = 200

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
    b1_volt_thread.end_thread()
    b2_volt_thread.end_thread() 
    b3_volt_thread.end_thread()
    b4_volt_thread.end_thread()
    validator_thread.end_thread()
    pressure_thread.end_thread()
    app.end_process()
    root.quit()
    root.destroy()
        
if __name__ == "__main__":

    temp1_values  = read_sensor_info("temp1.csv")
    b1_temp_thread = Monitor_thread(battery_1_temp_queue, temp1_graph_queue, notification_queue, "temperature", 70,30, "temp1",  ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5,  safety_state=temp1_values[1],value_state=temp1_values[2])
    b1_temp_thread.start()   
    print("b1 temp thread started")
    temp2_values  = read_sensor_info("temp2.csv")
    b2_temp_thread = Monitor_thread(battery_2_temp_queue, temp2_graph_queue, notification_queue,  "temperature", 70,30, "temp2",  ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5,  safety_state=temp2_values[1],value_state=temp2_values[2])
    b2_temp_thread.start()
    print("b2 temp thread started")
    temp3_values  = read_sensor_info("temp3.csv")
    b3_temp_thread = Monitor_thread(battery_3_temp_queue, temp3_graph_queue, notification_queue, "temperature", 70,30, "temp3", ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5,  safety_state=temp3_values[1],value_state=temp3_values[2])
    b3_temp_thread.start()
    print("b4 temp thread started")
    temp4_values  = read_sensor_info("temp4.csv")
    b4_temp_thread = Monitor_thread(battery_4_temp_queue, temp4_graph_queue, notification_queue, "temperature", 70,30, "temp4", ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5,  safety_state=temp4_values[1],value_state=temp4_values[2])
    b4_temp_thread.start()
    print("b4 temp thread started")
    volt1_values  = read_sensor_info("volt1.csv")
    b1_volt_thread = Monitor_thread(battery_1_volt_queue, volt1_graph_queue, notification_queue, "voltage", 4, 0, "volt1", ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5,  safety_state=volt1_values[1],value_state=volt1_values[2])
    b1_volt_thread.start()
    print("b1 volt thread started")
    volt2_values  = read_sensor_info("volt2.csv")
    b2_volt_thread = Monitor_thread(battery_2_volt_queue, volt2_graph_queue, notification_queue, "voltage", 4, 0, "volt2", ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5, safety_state=volt2_values[1], value_state=volt2_values[2])
    b2_volt_thread.start()
    print("b2 volt thread started")
    volt3_values  = read_sensor_info("volt3.csv")
    b3_volt_thread = Monitor_thread(battery_3_volt_queue, volt3_graph_queue, notification_queue, "voltage", 4, 0, "volt3", ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5,  safety_state=volt3_values[1], value_state=volt3_values[2])
    b3_volt_thread.start()
    print("b3 volt thread started")
    volt4_values  = read_sensor_info("volt4.csv")
    b4_volt_thread = Monitor_thread(battery_4_volt_queue, volt4_graph_queue, notification_queue, "voltage", 4, 0, "volt4",ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5, safety_state=volt4_values[1], value_state=volt4_values[2])
    b4_volt_thread.start()
    print("b4 volt thread started")
    pressure_values  = read_sensor_info("pressure.csv")
    pressure_thread = Monitor_thread(pressure_queue,pressure_graph_queue, notification_queue, "pressure", 100, 50, "pressure", ejection_time=ejection_time, monitor_length=monitor_length, error_length=error_length, timer=0.5, safety_state=pressure_values[1],value_state=pressure_values[2])
    pressure_thread.start()
    print("pressure thread started")
    validator_thread = Validator(queue_map)
    validator_thread.start()
    print("validator thread started")
    root = tk.Tk()
    root.title("Battery Monitor")
    root.geometry("1200x1000")  
    root.resizable(False, False) 
    app = UI(root,temp1_graph_queue, temp2_graph_queue, temp3_graph_queue, temp4_graph_queue, volt1_graph_queue, volt2_graph_queue, volt3_graph_queue, volt4_graph_queue, pressure_graph_queue, notification_queue, ejection_time, monitor_length, error_length)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    print("started GUI")
