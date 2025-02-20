import threading
import queue
import random
import time 
import tkinter as tk
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from xml.etree.ElementTree import TreeBuilder

from matplotlib.cbook import safe_first_element
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

# make my graphs and have a map for accesssin them


#-------------------------------------------------Validator---------------------------------------------------------------------------#

def start_up():
    while(True):
        incoming_data = "t1," + str(random.randint(30,70)) + ",v1," + str(random.randint(0,3)) + ", " 
        + "t2," + str(random.randint(30,70)) + ",v2," + str(random.randint(0,3)) + ", "
        + "t3," + str(random.randint(30,70))+ ",v3," + str(random.randint(0,3)) + ", "
        + "t4," + str(random.randint(30,70)) + ",v4," + str(random.randint(0,3)) + ", "
        + "p," + str(random.randint(50,100))  
        validate_data(incoming_data)
        

def validate_data(data):
    data_split = data.split(',')
    sensor_data = []
    while len(data_split) > 0:
        sensor_id = data_split.pop(0)
        sensor_data = data_split.pop(0)
        if (sensor_id == "t1" or sensor_id == "t2" or sensor_id == "t3" or sensor_id == "t4"):   
            if(isfloat(sensor_data)):
                queue_map[sensor_id].put((sensor_id,"temperature",sensor_data,"valid"))
            else:
                queue_map[sensor_id].put((sensor_id,"temperature",sensor_data,"invalid"))
        if (sensor_id == "v1" or sensor_id == "v2" or sensor_id == "v3" or sensor_id == "v4"):    
            if(isfloat(sensor_data)):
                queue_map[sensor_id].put((sensor_id,"voltage",sensor_data,"valid"))
            else:
                queue_map[sensor_id].put((sensor_id,"voltage",sensor_data,"invalid"))
        else:  
            if(isfloat(sensor_data)):
                queue_map[sensor_id].put((sensor_id,"pressure",sensor_data,"valid"))
            else:
                queue_map[sensor_id].put((sensor_id,"pressure",sensor_data,"invalid"))

def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

#---------------------------------------------------monitor----------------------------------------------------------------------------------#

class Monitor_thread(threading.Thread):
    
    def __init__(self, queue, graph, datatype, datatype_max, datatype_min):
        self.queue = queue_map(queue)
        self.monitor_values = {}
        self.error_values = {}
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
        #self.graph = graph_map(graph)
        
    def run(self):
        while(True):
            if not self.queue.empty():
                sensor_data = self.queue.get()
                if self.value_state == "safe":
                    # turn off mosfet
                    pass
                if self.safety_state == "eject":
                    pass
                if ((self.datatype_min <= sensor_data or sensor_data <= self.datatype_max ) and sensor_data(3) != "invalid"):
                    self.monitor_values.append(sensor_data(2))
                    # add the sensor_data to the graph
                    if (self.monitor_counter < 1000):
                        self.monitor_counter  = self.monitor_counter + 1
                    if (self.monitor_counter == 1000):
                        self.value_state = "safe"                  
                else:
                    current_error_type = None
                    if sensor_data(3) == "invalid":
                        #self.monitor_values.append() figure out the value for invalid data
                        self.error_values.append((sensor_data(2),"invalid"))
                        # add error value to graph figure otu what error value is
                        current_error_type = "invalid"
                    if sensor_data(2) < self.datatype_min:
                        self.error_values.append((sensor_data(2),"under"))
                        self.monitor_values.append((sensor_data(2)))
                        current_error_type = "under"
                        # add the sensor_data to the graph
                    if sensor_data(2) > self.datatype_max:
                        self.error_values.append((sensor_data(2),"over"))
                        self.monitor_values.append((sensor_data(2)))
                        current_error_type = "over"
                        # add the sensor_data to the graph
                    self.monitor_counter = 0
                    self.value_state = "unsafe"
                
                if float(self.error_counter / len(self.error_values)) <= 0.80:
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
                        
#------------------------------------------------------UI------------------------------------------------------------------------------------#

class UI:
    
    def __init__(self, root):
        self.graph_types = {
            "temperature": ["t1", "t2", "t3", "t4"],
            "voltage": ["v1", "v2", "v3", "v4"],
            "pressure": ["p1"],
        }
        
        self.main_frame = tk.Frame(root, bg="white", width=800,height=100)
        self.main_frame.pack()
        
        # frame for all buttons
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack()
        
        
        # frame for type buttons
        self.button_type_frame = tk.Frame(self.buttons_frame)
        self.button_type_frame.pack()
        
        #create graph selection button frame
        self.temp_button_frame = tk.Frame(self.button_type_frame, bg="blue", width=800, height=100)
        self.volt_button_frame = tk.Frame(self.button_type_frame, bg="blue", width=800, height=100)
        self.press_button_frame = tk.Frame(self.button_type_frame, bg="blue", width=800, height=100)
        
    
        self.type_buttons = {}
        #generate graph type buttons
        for graph_type in self.graph_types.keys():
            btn = tk.Button(
                self.button_type_frame,
                text=graph_type,
                command=lambda g_type=graph_type: self.show_graph_buttons(g_type),
                bg="lightgray",
            )
            btn.pack(side="left", pady=10, padx=10, fill="x")
            self.type_buttons[graph_type] = btn 
        
        self.graph_type_to_frame = {"temperature":self.temp_button_frame,
                                    "voltage":self.volt_button_frame,
                                    "pressure":self.press_button_frame}
        
        self.graph_type_to_graph_button = {"temperature":[],
                                    "voltage":[],
                                    "pressure":[]}
        
        # need to create my graphs
        self.graph_buttons = {}
        for graph in self.graphs.values():      
            btn = tk.Button(
                self.graph_type_to_frame[graph.data_type],
                text=graph.graph_id,
                command=lambda g_id=graph.graph_id, button=btn: self.show_graph(g_id, btn),
                bg="lightgray",
            )
            self.graph_type_to_graph_button[graph.data_type].append(graph.graph_id)
            
        #frame for graph buttons
        self.graph_button_frame = tk.Frame(self.buttons_frame)
        self.graph_button_frame.pack()
        
        #frame for graphs
        self.graph_frame = tk.Frame(self.main_frame)
        self.graph_frame.pack()
        
        self.temp_graph_frame = tk.Frame(self.graph_frame)
        self.volt_graph_frame = tk.Frame(self.graph_frame)
        self.pressure_graph_frame = tk.Frame(self.graph_frame)
        
        #add the queues 
        volt1_graph_frame = Graph_Frame("volt1","voltage",self.volt_graph_frame, volt1_graph_queue) 
        volt2_graph_frame = Graph_Frame("volt2","voltage",self.volt_graph_frame, volt2_graph_queue)
        volt3_graph_frame = Graph_Frame("volt3","voltage",self.volt_graph_frame, volt3_graph_queue)
        volt4_graph_frame = Graph_Frame("volt4","voltage",self.volt_graph_frame, volt4_graph_queue)
        
        temp1_graph_frame = Graph_Frame("temp1","temperature",self.temp_graph_frame, temp1_graph_queue)
        temp2_graph_frame = Graph_Frame("temp2","temperature",self.temp_graph_frame, temp2_graph_queue)
        temp3_graph_frame = Graph_Frame("temp3","temperature",self.temp_graph_frame, temp3_graph_queue)
        temp4_graph_frame = Graph_Frame("temp4","temperature",self.temp_graph_frame, temp4_graph_queue)
        
        pressure_graph_frame = Graph_Frame("pressure","pressure",self.pressure_graph_frame, pressure_graph_queue)    
        
        self.graph = {"temp": , "temp":, "temp":, "temp":, "volt":, "volt":, "volt":, "volt":, "pressure":}
                             
        
        #frame for notications
        self.notification_frame = tk.Frame(self.main_frame)
        self.notification_frame.pack()
        
    def display_notification(string):
        # figure out how to put a message in the notification frame
        
    
    def show_graph_buttons(self,graph_type):
        for frame in self.graph_type_to_frame.values():
            frame.pack_forget()
        for graph_t in self.graph_types.keys():
            if graph_t != graph_type:
                # i need to go through each graph of the type and turn them off
                for g in self.graph_type_to_graph_button[graph_t]:
                    self.graph_manager.hide_graph(g)                    
        self.graph_type_to_frame[graph_type].pack()
        
        
#-------------------------------- Graphs ----------------------------------------------------

class Graph_Frame:
    def __init__(self, graph_id, data_type, parent_frame, data_queue):
        self.graph_id = graph_id
        self.data_type = data_type
        self.data = None # might have  a backup csv
        self.canvas = None
        self.canvas_widget = None
        self.state = False
        self.data_queue = data_queue
        self.graph_frame = tk.Frame(parent_frame)
        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label=f"Graph {graph_id}")
        self.ax.legend()
        self.ax.set_title(f"Graph {graph_id} - {data_type}")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill='both', expand=True)
        self.canvas.draw()
    
    def update_data(self, new_data):
        self.data.append(new_data)  
        self.line.set_xdata(range(len(self.data)))
        self.line.set_ydata(self.data)  
        self.ax.relim()  
        self.ax.autoscale_view()

    def show(self):
        self.graph_frame.pack()
        
    def hide(self):
        self.graph_frame.pack_forget()
    
    def checkQueue(self):
        if self.data_queue:
            update_data(self.data_queue.pop()) # figure out this
            
    def getFrame(self):
        return self.graph_frame
