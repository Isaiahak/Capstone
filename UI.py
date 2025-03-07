from Graph_Frame import Graph_Frame
import time 
import tkinter as tk
import matplotlib
import os
matplotlib.use('TkAgg')
class UI:
    
    def __init__(self, root,temp1_graph_queue, temp2_graph_queue, temp3_graph_queue, temp4_graph_queue, volt1_graph_queue, volt2_graph_queue, volt3_graph_queue, volt4_graph_queue, pressure_graph_queue, notification_queue, configuration):
        self.is_running = True
        self.configuration = configuration
        self.root = root
        self.main_frame = tk.Frame(root, bg="gray", width=1200,height=1000)
        self.main_frame.pack(fill=tk.BOTH)
        self.notification_queue = notification_queue
    
        # frame for all buttons
        self.buttons_frame = tk.Frame(self.main_frame, bg="gray", width=1200, height=100)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)
        
        #frame for graphs
        self.graph_frame = tk.Frame(self.main_frame,bg="gray", width=1200, height=600)
        self.graph_frame.pack(side=tk.TOP, fill=tk.X)
        
        #frame for notications frames
        self.notification_frame = tk.Frame(self.main_frame, bg="gray", width=1200, height=1000)

        self.notification_button_frame = tk.Frame(self.notification_frame, bg="gray", width=1200, height=100)
        #self.notification_button_frame.pack(side=tk.TOP)
        self.ejection_notification_frame = tk.Frame(self.notification_frame,width=1200, height=900)
        self.mosfet_notification_frame = tk.Frame(self.notification_frame,width=1200, height=900)
        self.history_notification_frame = tk.Frame(self.notification_frame,width=1200, height=900)
        tk.Button(self.history_notification_frame, text="get history", command=lambda : self.get_history(), width=40,
                height=5, bg="lightgray").pack(side="left",pady=10, padx=10)
        
        self.text_frame = tk.Text(self.notification_frame, bg="gray", height=5, width=50)

        # frame for settings 
        self.setting_frame = tk.Frame(self.main_frame, bg="gray", width=1200, height=1000)

        self.monitor_length_frame = tk.Frame(self.setting_frame, bg="gray", width=1200, height=333).pack(side=tk.TOP)
        self.monitor_length_value = tk.Text(self.monitor_length_frame).pack(side="left")
        tk.Button(self.monitor_length_frame, text="monitor length",command= lambda s = "monitor length": self.change_settings(s), bg="lightgray").pack(side="left",pady=10, padx=50)
        
        self.error_length_frame = tk.Frame(self.setting_frame, bg="gray", width=1200, height=333).pack(side=tk.TOP)
        self.error_length_value = tk.Text(self.error_length_frame).pack(side="left")
        tk.Button(self.error_length_frame, text="error length",command= lambda s = "error length": self.change_settings(s), bg="lightgray").pack(side="left",pady=10, padx=50)
        
        self.ejection_time_frame = tk.Frame(self.setting_frame, bg="gray", width=1200, height=333).pack(side=tk.TOP)
        self.ejection_time_value = tk.Text(self.ejection_time_frame).pack(side="left")
        tk.Button(self.ejection_time_frame, text="ejection time",command= lambda s = "ejection time": self.change_settings(s), bg="lightgray").pack(side="left",pady=10, padx=50)
        
        # frame for type buttons
        self.button_type_frame = tk.Frame(self.buttons_frame, bg="gray", width=1200, height=50)
        self.button_type_frame.pack(side=tk.TOP)
        
         #frame for graph buttons
        self.graph_button_frame = tk.Frame(self.buttons_frame, bg="gray", width=1200, height=50)
        self.graph_button_frame.pack(side=tk.TOP, fill=tk.X)
        
        #create graph selection button frame
        self.temp_button_frame = tk.Frame(self.graph_button_frame, bg="gray", width=1200, height=50)
        self.volt_button_frame = tk.Frame(self.graph_button_frame, bg="gray", width=1200, height=50)
        self.press_button_frame = tk.Frame(self.graph_button_frame, bg="gray", width=1200, height=50)
        
        #frame for each graph type
        self.temp_graph_frame = tk.Frame(self.graph_frame,bg="gray", width=1200, height=300)
        self.volt_graph_frame = tk.Frame(self.graph_frame,bg="gray", width=1200, height=300)
        self.pressure_graph_frame = tk.Frame(self.graph_frame,bg="gray", width=1200, height=300)
        
        self.temp_graph_frame2 = tk.Frame(self.graph_button_frame,bg="gray", width=1200, height=300)
        self.volt_graph_frame2 = tk.Frame(self.graph_button_frame,bg="gray", width=1200, height=300)
        self.pressure_graph_frame2 = tk.Frame(self.graph_button_frame,bg="gray", width=1200, height=300) 
        
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

        self.notification_list = []
        #Structure which hold the graphs
        self.graph_map = {"temp1": self.temp1_graph_frame, "temp2": self.temp2_graph_frame, "temp3": self.temp3_graph_frame, "temp4": self.temp4_graph_frame, "volt1": self.volt1_graph_frame, "volt2": self.volt2_graph_frame, "volt3": self.volt3_graph_frame, "volt4": self.volt4_graph_frame, "pressure": self.press_graph_frame}                    
        self.graph_types_map = {"temperature": [self.temp1_graph_frame,self.temp2_graph_frame,self.temp3_graph_frame,self.temp4_graph_frame], "voltage": [self.volt1_graph_frame,self.volt2_graph_frame,self.volt3_graph_frame,self.volt4_graph_frame], "pressure": [self.pressure_graph_frame]}
    
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

        self.graph_display = {self.pressure_graph_frame : len(self.pressure_graph_frame.winfo_children()),self.volt_graph_frame : len(self.volt_graph_frame.winfo_children()), self.temp_graph_frame : len(self.temp_graph_frame.winfo_children()),
                                self.pressure_graph_frame2 : len(self.pressure_graph_frame2.winfo_children()), self.volt_graph_frame2 : len(self.volt_graph_frame2.winfo_children()), self.temp_graph_frame2 : len(self.temp_graph_frame2.winfo_children())}
        
        #generates a button for each graph type
        
        for graph_type in self.graph_type_to_frame.keys():
            tk.Button(
                self.button_type_frame,
                text=graph_type,
                command=lambda gt = graph_type: self.show_graph_type_buttons(gt),
                bg="lightgray",
            ).pack(side="left",pady=10, padx=50)
        tk.Button(self.button_type_frame, text="alerts",command= lambda : self.show_notification_frame(), bg="lightgray").pack(side="left",pady=10, padx=50)
        tk.Button(self.button_type_frame, text="settings",command= lambda : self.show_settings_frame(), bg="lightgray").pack(side="left",pady=10, padx=50)

        #generates a button for each graph
        for graph in self.graph_map.keys():
            if (graph[0:4] == "temp"):
                graph_type = "temperature"
            if(graph[0:4] == "volt"):
                graph_type = "voltage" 
            if(graph[0:4] == "pres"):
                graph_type = "pressure"    
            tk.Button(
                self.graph_type_to_frame[graph_type],
                text=graph,
                command=lambda  g = graph: self.show_graph_buttons(g),
                bg="lightgray",
            ).pack(side="left",pady=10, padx=50)        
        self.update_graph()

        #notification buttons
        tk.Button(self.notification_button_frame, text="mosfet", command=lambda type="mosfet": self.show_specific_notification_type(type), width=40,
                height=5, bg="lightgray").pack(side="left",pady=10, padx=50)
        tk.Button(self.notification_button_frame, text="ejection", command=lambda type="ejection": self.show_specific_notification_type(type), width=40,
                height=5, bg="lightgray").pack(side="left",pady=10, padx=10)
        tk.Button(self.notification_button_frame, text="notification history", command=lambda type="history": self.show_specific_notification_type(type), width=40,
                height=5, bg="lightgray").pack(side="left",pady=10, padx=10)
        
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
        while not self.notification_queue.empty():
            notifications = self.notification_queue.get()
            self.notification_list.append(notifications)
            if notifications.get_notification_type() == "ejection":
                if (len(self.ejection_notification_frame.winfo_children()) > 10):
                    self.ejection_notification_frame.winfo_children().pop(0)
                notifications.create(self.ejection_notification_frame)
            else:
                if (len(self.mosfet_notification_frame.winfo_children()) > 10):
                    self.mosfet_notification_frame.winfo_children().pop(0)
                notifications.create(self.mosfet_notification_frame)
            notifications.get_frame().pack()
        
        for notification in self.notification_list:
            creation_time = notification.get_creation_time()
            if(time.time() - creation_time  > 1800):
                notification.get_frame().destroy()
        if(self.is_running):
            self.root.after(350, self.update_graph)

    def show_graph_buttons(self,graph): 
        graph_frame = self.graph_map[graph].get_frame()
        if(self.graph_map[graph].get_state() == False):
            self.graph_map[graph].set_state(True)  
            graph_frame.pack(side=tk.LEFT)       
        else:
            self.graph_map[graph].set_state(False)
            graph_frame.pack_forget()
            
    def show_graph_type_buttons(self,graph_type):
        self.notification_frame.pack_forget()
        self.setting_frame.pack_forget()
        self.graph_frame.pack(side=tk.TOP, fill=tk.X)
        self.graph_button_frame.pack(side=tk.TOP, fill=tk.X)
        for frame in self.graph_type_to_frame.values():
            frame.pack_forget()
        for frame in self.graph_type_to_graph_frame.values():
            frame.pack_forget()
        for frame in self.graph_type_to_graph_frame2.values():
            frame.pack_forget()
        for graph in self.graph_map.values():
            graph.set_state(False)
            graph.get_frame().pack_forget()
        self.graph_type_to_frame[graph_type].pack(side=tk.TOP)
        self.graph_type_to_graph_frame[graph_type].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)   
        self.graph_type_to_graph_frame2[graph_type].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)   

    def show_specific_notification_type(self, notification_type):
        if(notification_type == "mosfet"):
            self.ejection_notification_frame.pack_forget()
            self.history_notification_frame.pack_forget()
            self.mosfet_notification_frame.pack()
        elif (notification_type == "ejection"):
            self.mosfet_notification_frame.pack_forget()
            self.history_notification_frame.pack_forget()
            self.ejection_notification_frame.pack()
        else:
            self.mosfet_notification_frame.pack_forget()
            self.ejection_notification_frame.pack_forget()
            self.history_notification_frame.pack()

    def get_history(self):
        os.startfile("notification_logs.csv")

    def show_notification_frame(self):
        self.graph_frame.pack_forget()
        self.graph_button_frame.pack_forget()
        self.setting_frame.pack_forget()
        self.notification_frame.pack(side=tk.TOP, fill=tk.X)
        print("notification")

    def show_settings_frame(self):
        self.graph_frame.pack_forget()
        self.graph_button_frame.pack_forget()
        self.notification_frame.pack_forget()
        self.setting_frame.pack(side=tk.TOP, fill=tk.X)
        print("settings")

    def change_settings(self, setting):
        if(setting == "error_length"):
            value = self.error_length_value.get("1.0",tk.END)
            if (   50  < value  < 400 ):
                self.configuration.set_error_length(value)  
        elif( setting == "monitor_length"):
            value = self.monitor_length_value.get("1.0",tk.END)
            if ( 500 < value < 2000):
                self.configuration.set_monitor_length(value)
        elif(setting == "ejection_time"):
            value = self.ejection_time_value.get("1.0",tk.END)
            if (300 < value < 900):
                self.configuration.set_ejection_time(value)

    def end_process(self):
        self.is_running = False