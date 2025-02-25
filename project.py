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
        
    def run(self):
        while(self.is_running):
            incoming_data = "t1," + str(random.randint(30,70)) + ",v1," + str(random.randint(0,3)) + ",t2," + str(random.randint(30,70)) + ",v2," + str(random.randint(0,3)) + ",t3," + str(random.randint(30,70))+ ",v3," + str(random.randint(0,3)) + ",t4," + str(random.randint(30,70)) + ",v4," + str(random.randint(0,3)) + ",p," + str(random.randint(50,100))  
            self.validate_data(incoming_data)
            time.sleep(1000)
        print("thread ended")

    # added pass to remove pressure sensor
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
                pass
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
    
    def __init__(self, queue, graph_queue, datatype, datatype_max, datatype_min):
        super().__init__()
        self.queue = queue
        self.monitor_values = []
        self.error_values = []
        self.sensor_state = "valid"
        self.sensor_datatype = datatype
        self.datatype_max = datatype_max
        self.datatype_min = datatype_min
        self.monitor_counter = 0
        self.value_state = "safe"
        self.safety_state = None
        self.last_error_type = None
        self.error_counter = 0
        self.ejection_timer = None
        self.graph_queue = graph_queue 
        self.is_running = True
        
    def run(self):
        while(self.is_running == True):
            if not self.queue.empty():
                sensor_data = self.queue.get()
                value = float(sensor_data[2])
                if(len(self.monitor_values) > 999):
                    value_to_be_removed = self.monitor_values.pop(0)
                    if(value_to_be_removed in self.error_values):
                        self.error_values.remove(value_to_be_removed)
                if self.value_state == "safe":
                    # turn off mosfet
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
                    #see errors
                    print(sensor_data, time.time())

                if( len(self.error_values) > 0):
                    if float(self.error_counter / len(self.error_values)) <= 0.80 and  len(self.error_values) > 50:
                        if self.safety_state == None:
                            self.safety_state = "mosfet"
                            # turn on mosfet
                            self.ejection_timer = time.time()
                        if self.safety_state == "mosfet":
                            if ((time.time() - self.ejection_timer) < 60 ):
                                #notify UI with the time spend in the error state
                                pass
                            if ((time.time() - self.ejection_timer) >= 60):
                                #eject
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
            time.sleep(1000)
        print("thread ended")
                            
    def end_thread(self):
        self.is_running = False               
#------------------------------------------------------UI------------------------------------------------------------------------------------#
class UI:
    
    def __init__(self, root,temp1_graph_queue, temp2_graph_queue, temp3_graph_queue, temp4_graph_queue, volt1_graph_queue, volt2_graph_queue, volt3_graph_queue, volt4_graph_queue, pressure_graph_queue):
        self.root = root
        self.main_frame = tk.Frame(root, bg="gray", width=1800,height=1200)
        self.main_frame.pack()
        
        # frame for all buttons
        self.buttons_frame = tk.Frame(self.main_frame, width=1600, height=300)
        self.buttons_frame.pack(side=tk.TOP)
        
        # frame for type buttons
        self.button_type_frame = tk.Frame(self.buttons_frame, width=1600, height=100)
        self.button_type_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        
        #create graph selection button frame
        self.temp_button_frame = tk.Frame(self.button_type_frame, bg="darkgray", width=600, height=100)
        self.volt_button_frame = tk.Frame(self.button_type_frame, bg="darkgray", width=600, height=100)
        self.press_button_frame = tk.Frame(self.button_type_frame, bg="darkgray", width=600, height=100)
        
         #frame for graph buttons
        self.graph_button_frame = tk.Frame(self.buttons_frame)
        self.graph_button_frame.pack(side=tk.BOTTOM)
        
        #frame for graphs
        self.graph_frame = tk.Frame(self.main_frame)
        self.graph_frame.pack()
        
        #frame for each graph type
        self.temp_graph_frame = tk.Frame(self.graph_frame)
        self.volt_graph_frame = tk.Frame(self.graph_frame)
        self.pressure_graph_frame = tk.Frame(self.graph_frame)
        
        #frames of each graph
        self.volt1_graph_frame = Graph_Frame("volt1","voltage",self.volt_graph_frame, volt1_graph_queue) 
        self.volt2_graph_frame = Graph_Frame("volt2","voltage",self.volt_graph_frame, volt2_graph_queue)
        print("quarter way")
        self.volt3_graph_frame = Graph_Frame("volt3","voltage",self.volt_graph_frame, volt3_graph_queue)
        self.volt4_graph_frame = Graph_Frame("volt4","voltage",self.volt_graph_frame, volt4_graph_queue)
        print("half way")
        self.temp1_graph_frame = Graph_Frame("temp1","temperature",self.temp_graph_frame, temp1_graph_queue)
        self.temp2_graph_frame = Graph_Frame("temp2","temperature",self.temp_graph_frame, temp2_graph_queue)
        print("3 quarters way")
        self.temp3_graph_frame = Graph_Frame("temp3","temperature",self.temp_graph_frame, temp3_graph_queue)
        self.temp4_graph_frame = Graph_Frame("temp4","temperature",self.temp_graph_frame, temp4_graph_queue)
        self.pressure_graph_frame = Graph_Frame("pressure","pressure",self.pressure_graph_frame, pressure_graph_queue)    
        print("done graph frames")

        #frame for notications
        self.notification_frame = tk.Frame(self.main_frame, width=1600, height=100)
        self.notification_frame.pack(side=tk.BOTTOM)

        #Structure which hold the graphs
        self.graph_map = {"temp1": self.temp1_graph_frame, "temp2": self.temp2_graph_frame, "temp": self.temp3_graph_frame, "temp4": self.temp4_graph_frame, "volt1": self.volt1_graph_frame, "volt2": self.volt2_graph_frame, "volt3": self.volt3_graph_frame, "volt4": self.volt4_graph_frame, "pressure": self.pressure_graph_frame}                    
        self.graph_types_map = {"temperature": [self.temp1_graph_frame,self.temp2_graph_frame,self.temp3_graph_frame,self.temp4_graph_frame], "voltage": [self.volt1_graph_frame,self.volt2_graph_frame,self.volt3_graph_frame,self.volt4_graph_frame], "pressure": [self.pressure_graph_frame]}
    
        #Structure which hold button frames
        self.graph_type_to_frame = {"temperature":self.temp_button_frame,
                                    "voltage":self.volt_button_frame,
                                    "pressure":self.press_button_frame}
        
        #structure which holds the different buttons for each type
        self.graph_type_to_graph_button = {"temperature":[],
                                    "voltage":[],
                                    "pressure":[]}
        
        self.type_buttons = {}

    
        
        #generates a button for each graph type
        #added pass for pressure
        for graph_type in self.graph_types_map.keys():
            if (graph_type == "pressure"): 
                pass
            btn = tk.Button(
                self.button_type_frame,
                text=graph_type,
                command=lambda: self.show_graph_type_buttons(graph_type),
                bg="lightgray",
            )
            btn.pack(side="left", pady=10, padx=10)
            self.type_buttons[graph_type] = btn 
        
        
        #generates a button for each graph

        # added apss for pressure
        self.graph_buttons = {}
        for graph in self.graph_map.keys():
            if (graph == "pressure"):
                pass      
            btn = tk.Button(
                self.graph_map[graph],
                text=graph,
                command=lambda: self.show_graph_buttons(graph),
                bg="lightgray",
            )
            
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
        self.pressure_graph_frame.checkQueue()
        
        self.root.after(1000, self.update_graph)
            
    def show_graph_buttons(self,graph_type):
        if(self.graph_map[graph_type].get_state() == False):
            self.graph_map[graph_type].set_state(True)
            self.graph_map[graph_type].pack(side=tk.LEFTi) 
        else:
            self.graph_map[graph_type].set_state(False)
            self.graph_map[graph_type].pack_forget()
            pass

    def show_graph_type_buttons(self,graph_type):
        #turns of all of the graphs frames
        for frame in self.graph_type_to_frame.values():
            frame.pack_forget()
        #unpack all graphs associated with types not turned on
        for graph_t in self.graph_types_map.keys():
            if graph_t != graph_type:
                # i need to go through each graph of the type and turn them off
                for g in self.graph_types_map[graph_t]:
                    g.pack_forget()
        current_frame = self.graph_type_to_frame[graph_type]                                 
        current_frame.pack(side=tk.BOTTOM)

    def display_notification(self,string):
        # figure out how to put a message in the notification frame
        pass
#-------------------------------- Graphs ----------------------------------------------------
# call the checkqueue method externally in main thread on a timer figure this out
class Graph_Frame(tk.Frame):
    def __init__(self, graph_id, data_type, parent_frame, data_queue):
        super().__init__(parent_frame)
        self.graph_id = graph_id
        self.data_type = data_type
        self.data = [] # might have  a backup csv
        self.state = False
        self.data_queue = data_queue
        self.graph_frame = tk.Frame(parent_frame)
        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label=f"Graph {graph_id}")
        self.ax.legend()
        self.ax.set_title(f"Graph {graph_id} - {data_type}")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        if (data_type == "temperature"):
            self.ax.set_ylim(20,90)
        if (data_type == "voltage"):
            self.ax.set_ylim(-1,5)  
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill='both', expand=True)
        self.canvas.draw()
    
    def update_data(self, new_data):
        self.data.append(new_data)  
        self.line.set_xdata(range(len(self.data)))
        self.line.set_ydata(self.data)  
            
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

#application setup           
if __name__ == "__main__":
    b1_temp_thread = Monitor_thread(battery_1_temp_queue, temp1_graph_queue, "temperature", 70,30)
    b1_temp_thread.start()   
    print("b1 temp thread started")
    b2_temp_thread = Monitor_thread(battery_2_temp_queue, temp2_graph_queue, "temperature", 70,30)
    b2_temp_thread.start()
    print("b2 temp thread started")
    b3_temp_thread = Monitor_thread(battery_3_temp_queue, temp3_graph_queue, "temperature", 70,30)
    b3_temp_thread.start()
    print("b4 temp thread started")
    b4_temp_thread = Monitor_thread(battery_4_temp_queue, temp4_graph_queue, "temperature", 70,30)
    b4_temp_thread.start()
    print("b4 temp thread started")
    b1_volt_thread = Monitor_thread(battery_1_volt_queue, volt1_graph_queue,"voltage",4,0)
    b1_volt_thread.start()
    print("b1 volt thread started")
    b2_volt_thread = Monitor_thread(battery_2_volt_queue, volt2_graph_queue,"voltage",4,0)
    b2_volt_thread.start()
    print("b2 volt thread started")
    b3_volt_thread = Monitor_thread(battery_3_volt_queue, volt3_graph_queue,"voltage",4,0)
    b3_volt_thread.start()
    print("b3 volt thread started")
    b4_volt_thread = Monitor_thread(battery_4_volt_queue, volt4_graph_queue,"voltage",4,0)
    b4_volt_thread.start()
    print("b4 volt thread started")

    # commented out pressure
    #pressure_thread = Monitor_thread(pressure_queue,pressure_graph_queue,"pressure","","")
    #pressure_thread.start_monitor()

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
        #pressure_thread.end_thread()
        root.quit()
        root.destroy()
        
    root = tk.Tk()
    root.title("Battery Monitor")
    root.geometry("1600x1200")  
    root.resizable(False, False) 
    app = UI(root,temp1_graph_queue, temp2_graph_queue, temp3_graph_queue, temp4_graph_queue, volt1_graph_queue, volt2_graph_queue, volt3_graph_queue, volt4_graph_queue, pressure_graph_queue)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    print("started GUI")
    b1_temp_thread.join()
    b2_temp_thread.join()
    b3_temp_thread.join()
    b4_temp_thread.join()
    b1_volt_thread.join()
    b2_volt_thread.join()
    b3_volt_thread.join()
    b4_volt_thread.join()
    

    validator_thread.join()