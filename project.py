import threading
import queue
import random
import time 
import numpy as np
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
queue_map = {"v1" : battery_1_volt_queue,"v2" : battery_2_volt_queue, "v3" : battery_3_volt_queue, "v4" : battery_4_volt_queue,
             "t1" : battery_1_temp_queue, "t2" : battery_2_temp_queue, "t3" : battery_3_temp_queue, "t4" : battery_4_temp_queue,
             "p" : pressure_queue}
#-------------------------------------------------Validator---------------------------------------------------------------------------#
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
            incoming_data = "t1," + str(round(max(30, min(random.normalvariate(50, self.std_for_temperature),  80)))) + ",v1," + str(round(max(0, min(random.normalvariate(2, self.std_for_voltage),  5)))) + ",t2," + str(round(max(30, min(random.normalvariate(50, self.std_for_temperature),  80)))) + ",v2," + str(round(max(0, min(random.normalvariate(2, self.std_for_voltage),  5)))) + ",t3," + str(round(max(30, min(random.normalvariate(50, self.std_for_temperature),  80))))+ ",v3," + str(round(max(0, min(random.normalvariate(2, self.std_for_voltage),  5)))) + ",t4," + str(round(max(30, min(random.normalvariate(50, self.std_for_temperature),  80)))) + ",v4," + str(round(max(0, min(random.normalvariate(2, self.std_for_voltage),  5)))) + ",p," + str(round(max(50, min(random.normalvariate(75, self.std_for_pressure),  110))))  
            self.validate_data(incoming_data)
            time.sleep(1)
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
#---------------------------------------------------monitor----------------------------------------------------------------------------------#
class Monitor_thread(threading.Thread):
    
    def __init__(self, queue, graph_queue, datatype, datatype_max, datatype_min, monitor_id):
        super().__init__()
        self.queue = queue
        self.monitor_id = monitor_id
        self.monitor_values = []
        self.error_values = []
        self.sensor_state = "valid"
        self.sensor_datatype = datatype
        self.datatype_max = datatype_max
        self.datatype_min = datatype_min
        self.datatype = datatype
        self.monitor_counter = 0
        self.value_state = "safe"
        self.safety_state = None
        self.last_error_type = None
        self.error_counter = 0
        self.ejection_timer = None
        self.graph_queue = graph_queue 
        self.is_running = True
        self.safe_flag = True
        
    def run(self):
        while(self.is_running == True):
            if not self.queue.empty():
                sensor_data = self.queue.get()
                value = float(sensor_data[2])
                if(len(self.monitor_values) > 999):
                    value_to_be_removed = self.monitor_values.pop(0)
                    if(value_to_be_removed in self.error_values):
                        self.error_values.remove(value_to_be_removed)
                if (self.value_state == "safe" and self.safe_flag == False):
                    self.safe_flag = True
                    # turn off mosfet
                    print(self.monitor_id +" mostfet turned off")
                    pass
                if self.safety_state == "eject":
                    pass
                if ((self.datatype_min <= value or value <= self.datatype_max ) and sensor_data[3] != "invalid"):
                    self.monitor_values.append(value)
                    self.graph_queue.put(value)
                    if (self.monitor_counter < 1000):
                        self.monitor_counter  = self.monitor_counter + 1
                    if (self.monitor_counter == 1000):
                        self.value_state = "safe"                  
                else:
                    if (len(self.error_values) > 100):
                        self.error_values.pop(0)
                    current_error_type = None
                    if sensor_data[3] == "invalid":
                        self.monitor_values.append(np.nan)
                        self.error_values.append((value,"invalid"))
                        self.graph_queue.put(np.nan)
                        current_error_type = "invalid"
                    if value < self.datatype_min:
                        self.error_values.append((value,"under"))
                        self.monitor_values.append(value)
                        current_error_type = "under"
                        self.graph_queue.put(value)
                    if value > self.datatype_max:
                        self.error_values.append((value,"over"))
                        self.monitor_values.append(value)
                        current_error_type = "over"
                        self.graph_queue.put(value)
                    self.monitor_counter = 0
                    self.value_state = "unsafe"
                    self.safe_flag = False
                    #see errors
                    print(sensor_data, time.time())

                if( len(self.error_values) > 0):
                    if float(self.error_counter / len(self.error_values)) <= 0.80 and  len(self.error_values) > 50:
                        if self.safety_state == None:
                            self.safety_state = "mosfet"
                            # turn on mosfet
                            print(self.monitor_id +" mosfet triggered")
                            self.ejection_timer = time.time()
                        if self.safety_state == "mosfet":
                            if ((time.time() - self.ejection_timer) < 60 ):
                                #notify UI with the time spend in the error state
                                print(self.monitor_id + " ejection will commence in " + time.time() - self.ejection_timer)
                                pass
                            if ((time.time() - self.ejection_timer) >= 60):
                                #eject
                                print(self.monitor_id +" eject triggered")
                                # only if we eject set state to eject
                                self.safety_state = "eject"
                    else:
                        if self.last_error_type == None:
                            self.last_error_type = current_error_type
                        if self.last_error_type == current_error_type:
                            self.error_counter = self.error_counter + 1
                        else:
                            self.error_counter = 0 
                            self.last_error_type = current_error_type
            time.sleep(1)
        print("thread ended")
                            
    def end_thread(self):
        self.is_running = False               
#------------------------------------------------------UI------------------------------------------------------------------------------------#
class UI:
    
    def __init__(self, root,temp1_graph_queue, temp2_graph_queue, temp3_graph_queue, temp4_graph_queue, volt1_graph_queue, volt2_graph_queue, volt3_graph_queue, volt4_graph_queue, pressure_graph_queue):
        self.root = root
        self.main_frame = tk.Frame(root, bg="darkgray", width=1600,height=1200)
        self.main_frame.pack()
        
        # frame for all buttons
        self.buttons_frame = tk.Frame(self.main_frame, width=1600, height=200)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)
        
        #frame for graphs
        self.graph_frame = tk.Frame(self.main_frame,bg="gray", width=1600, height=800)
        self.graph_frame.pack(side=tk.TOP, fill=tk.X)
        
         #frame for notications
        self.notification_frame = tk.Frame(self.main_frame, width=1600, height=100, bg="darkgray")
        self.notification_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # frame for type buttons
        self.button_type_frame = tk.Frame(self.buttons_frame, bg="lightgray", width=1600, height=100)
        self.button_type_frame.pack(side=tk.TOP, fill=tk.X)
        
         #frame for graph buttons
        self.graph_button_frame = tk.Frame(self.buttons_frame, width=1600, height=100)
        self.graph_button_frame.pack(side=tk.TOP, fill=tk.X)
        
        #create graph selection button frame
        self.temp_button_frame = tk.Frame(self.graph_button_frame, bg="darkgray", width=1600, height=100)
        self.volt_button_frame = tk.Frame(self.graph_button_frame, bg="darkgray", width=1600, height=100)
        self.press_button_frame = tk.Frame(self.graph_button_frame, bg="darkgray", width=1600, height=100)
        
        #frame for each graph type
        self.temp_graph_frame = tk.Frame(self.graph_frame,bg="gray", width=1600, height=400)
        self.volt_graph_frame = tk.Frame(self.graph_frame,bg="gray", width=1600, height=400)
        self.pressure_graph_frame = tk.Frame(self.graph_frame,bg="gray", width=1600, height=400)
        
        self.temp_graph_frame2 = tk.Frame(self.graph_button_frame,bg="gray", width=1600, height=400)
        self.volt_graph_frame2 = tk.Frame(self.graph_button_frame,bg="gray", width=1600, height=400)
        self.pressure_graph_frame2 = tk.Frame(self.graph_button_frame,bg="gray", width=1600, height=400) 
        
        
        #frames of each graph
        self.volt1_graph_frame = Graph_Frame("volt1","voltage",self.volt_graph_frame, volt1_graph_queue) 
        self.volt2_graph_frame = Graph_Frame("volt2","voltage",self.volt_graph_frame, volt2_graph_queue)
        self.volt3_graph_frame = Graph_Frame("volt3","voltage",self.volt_graph_frame2, volt3_graph_queue)
        self.volt4_graph_frame = Graph_Frame("volt4","voltage",self.volt_graph_frame2, volt4_graph_queue)
        self.temp1_graph_frame = Graph_Frame("temp1","temperature",self.temp_graph_frame, temp1_graph_queue)
        self.temp2_graph_frame = Graph_Frame("temp2","temperature",self.temp_graph_frame, temp2_graph_queue)
        self.temp3_graph_frame = Graph_Frame("temp3","temperature",self.temp_graph_frame2, temp3_graph_queue)
        self.temp4_graph_frame = Graph_Frame("temp4","temperature",self.temp_graph_frame2, temp4_graph_queue)
        self.press_graph_frame = Graph_Frame("pressure","pressure",self.pressure_graph_frame, pressure_graph_queue)    

        #Structure which hold the graphs
        self.graph_map = {"temp1": self.temp1_graph_frame, "temp2": self.temp2_graph_frame, "temp3": self.temp3_graph_frame, "temp4": self.temp4_graph_frame, "volt1": self.volt1_graph_frame, "volt2": self.volt2_graph_frame, "volt3": self.volt3_graph_frame, "volt4": self.volt4_graph_frame, "pressure": self.press_graph_frame}                    
        #self.graph_types_map = {"temperature": [self.temp1_graph_frame,self.temp2_graph_frame,self.temp3_graph_frame,self.temp4_graph_frame], "voltage": [self.volt1_graph_frame,self.volt2_graph_frame,self.volt3_graph_frame,self.volt4_graph_frame], "pressure": [self.pressure_graph_frame]}
    
        #Structure which hold button frames
        self.graph_type_to_frame = {"temperature":self.temp_button_frame,
                                    "voltage":self.volt_button_frame,
                                    "pressure":self.press_button_frame}
        
        self.graph_type_to_graph_frame = {"temperature":self.temp_graph_frame,
                                          "voltage":self.volt_graph_frame,
                                          "pressure":self.pressure_graph_frame}
        
        self.graph_type_to_graph_frame2 = {"temperature":self.temp_graph_frame2,
                                          "voltage":self.volt_graph_frame2,
                                          "pressure":self.pressure_graph_frame2}
        
        #generates a button for each graph type
        for graph_type in self.graph_type_to_frame.keys():
            btn = tk.Button(
                self.button_type_frame,
                text=graph_type,
                command=lambda gt = graph_type: self.show_graph_type_buttons(gt),
                bg="lightgray",
            ).pack(side="left",pady=10, padx=50)
        
        #generates a button for each graph
        for graph in self.graph_map.keys():
            if (graph[0:4] == "temp"):
                graph_type = "temperature"
            if(graph[0:4] == "volt"):
                graph_type = "voltage" 
            if(graph[0:4] == "pres"):
                graph_type = "pressure"    
            btn = tk.Button(
                self.graph_type_to_frame[graph_type],
                text=graph,
                command=lambda  g = graph: self.show_graph_buttons(g),
                bg="gray",
            ).pack(side="left",pady=10, padx=50)
                
        
        self.update_graph()

    def update_graph(self):
        self.volt1_graph_frame.checkQueue()
        self.volt2_graph_frame.checkQueue()
        self.volt3_graph_frame.checkQueue()
        self.volt4_graph_frame.checkQueue()
        self.temp1_graph_frame.checkQueue()
        self.temp2_graph_frame.checkQueue()
        self.temp3_graph_frame.checkQueue()
        self.temp4_graph_frame.checkQueue()
        self.press_graph_frame.checkQueue()
        self.root.after(1000, self.update_graph)
            
    def show_graph_buttons(self,graph): 
        graph_frame = self.graph_map[graph].get_frame()
        if(self.graph_map[graph].get_state() == False):
            self.graph_map[graph].set_state(True)  
            graph_frame.pack(side=tk.LEFT)       
        else:
            self.graph_map[graph].set_state(False)
            graph_frame.pack_forget()
            self.root.update()

    def show_graph_type_buttons(self,graph_type):
        #turns of all of the graphs frames
        for frame in self.graph_type_to_frame.values():
            frame.pack_forget()
        for frame in self.graph_type_to_graph_frame.values():
            frame.pack_forget()
        for frame in self.graph_type_to_graph_frame2.values():
            frame.pack_forget()
        self.graph_type_to_frame[graph_type].pack(side=tk.TOP, fill=tk.X)
        self.graph_type_to_graph_frame[graph_type].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)   
        self.graph_type_to_graph_frame2[graph_type].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)                             
        
    def display_notification(self,string):
        # figure out how to put a message in the notification frame
        pass
#------------------------------------------------- Graphs ------------------------------------------------------------#
class Graph_Frame(tk.Frame):
    def __init__(self, graph_id, data_type, parent_frame, data_queue):
        super().__init__(parent_frame)
        self.graph_id = graph_id
        self.data_type = data_type
        self.data = [] # might have  a backup csv
        self.state = False
        self.data_queue = data_queue
        self.graph_frame = tk.Frame(parent_frame, width=800, height=400)
        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.data, label=f"Graph {graph_id}")
        self.ax.legend()
        self.ax.set_title(f"Graph {graph_id} - {data_type}")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis") 
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()
    
    def update_data(self, new_data, max_points=100):
        self.data.append(new_data)
        if len(self.data) > max_points:
            self.data.pop(0)
        self.line.set_xdata(range(len(self.data)))
        self.line.set_ydata(self.data)
        if (self.data_type == "temperature"):
            self.ax.set_ylim(20,90)
        if (self.data_type == "voltage"):
            self.ax.set_ylim(-1,5)
        if (self.data_type == "pressure"):
            self.ax.set_ylim(40,110)
        self.ax.set_xlim(0, len(self.data))
        self.canvas.draw() 
                
    def get_frame(self):
        return self.graph_frame
    
    def get_state(self):
        return self.state
    
    def set_state(self, state):
        if (state == True or state == False):
            self.state = state

    def checkQueue(self):
        if not self.data_queue.empty():
            self.update_data(self.data_queue.get())        
#-----------------------------------------------#application setup#-----------------------------------------------------------#        
if __name__ == "__main__":
    b1_temp_thread = Monitor_thread(battery_1_temp_queue, temp1_graph_queue, "temperature", 70,30, "temp1")
    b1_temp_thread.start()   
    print("b1 temp thread started")
    b2_temp_thread = Monitor_thread(battery_2_temp_queue, temp2_graph_queue, "temperature", 70,30, "temp2")
    b2_temp_thread.start()
    print("b2 temp thread started")
    b3_temp_thread = Monitor_thread(battery_3_temp_queue, temp3_graph_queue, "temperature", 70,30, "temp3")
    b3_temp_thread.start()
    print("b4 temp thread started")
    b4_temp_thread = Monitor_thread(battery_4_temp_queue, temp4_graph_queue, "temperature", 70,30, "temp4")
    b4_temp_thread.start()
    print("b4 temp thread started")
    b1_volt_thread = Monitor_thread(battery_1_volt_queue, volt1_graph_queue,"voltage",4,0, "volt1")
    b1_volt_thread.start()
    print("b1 volt thread started")
    b2_volt_thread = Monitor_thread(battery_2_volt_queue, volt2_graph_queue,"voltage",4,0, "volt2")
    b2_volt_thread.start()
    print("b2 volt thread started")
    b3_volt_thread = Monitor_thread(battery_3_volt_queue, volt3_graph_queue,"voltage",4,0, "volt3")
    b3_volt_thread.start()
    print("b3 volt thread started")
    b4_volt_thread = Monitor_thread(battery_4_volt_queue, volt4_graph_queue,"voltage",4,0, "volt4")
    b4_volt_thread.start()
    print("b4 volt thread started")
    pressure_thread = Monitor_thread(pressure_queue,pressure_graph_queue,"pressure",100,50, "pressure")
    pressure_thread.start()
    print("pressure thread started")
    validator_thread = Validator(queue_map)
    validator_thread.start()
    print("validator thread started")
    
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
        
        root.quit()
        root.destroy()
        
    root = tk.Tk()
    root.title("Battery Monitor")
    root.geometry("1600x1200")  
    root.resizable(True, True) 
    app = UI(root,temp1_graph_queue, temp2_graph_queue, temp3_graph_queue, temp4_graph_queue, volt1_graph_queue, volt2_graph_queue, volt3_graph_queue, volt4_graph_queue, pressure_graph_queue)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    print("started GUI")
