import tkinter as tk
import threading
from Graphs import Graph, GraphManager, listen_to_socket

class GraphApp:
    def __init__(self, root):
        #graph buttons frame 
        self.graph_frame_frame = tk.Frame(root, bg="white", width=800,height=100)
        self.graph_frame_frame.pack_propagate(False)
        self.graph_frame_frame.pack()

        # Initialize data
        self.graph_types = {
            "temperature": ["t1", "t2", "t3", "t4"],
            "voltage": ["v1", "v2", "v3", "v4"],
            "pressure": ["p1"],
        }

        #graph type button frame
        self.graph_type_frame = tk.Frame(self.graph_frame_frame)
        self.graph_type_frame.pack()
        
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack()
        self.graph_manager = GraphManager(self.graph_frame)
        self.graphs = self.graph_manager.get_graphs()
    
        # Start the socket listening thread
        socket_thread = threading.Thread(target=listen_to_socket, args=(self.graph_manager))
        socket_thread.daemon = True
        socket_thread.start()
    
        
        self.type_buttons = {}
        
        #generate graph type buttons
        for graph_type in self.graph_types.keys():
            btn = tk.Button(
                self.graph_type_frame,
                text=graph_type,
                command=lambda g_type=graph_type: self.show_graph_buttons(g_type),
                bg="lightgray",
            )
            btn.pack(side="left", pady=10, padx=10, fill="x")
            self.type_buttons[graph_type] = btn 

        #create graph selection button frame
        self.temp_button_frame = tk.Frame(self.graph_frame_frame, bg="blue", width=800, height=100)
        self.volt_button_frame = tk.Frame(self.graph_frame_frame, bg="blue", width=800, height=100)
        self.press_button_frame = tk.Frame(self.graph_frame_frame, bg="blue", width=800, height=100)

        self.graph_type_to_frame = {"temperature":self.temp_button_frame,
                                    "voltage":self.volt_button_frame,
                                    "pressure":self.press_button_frame}
        
        # creates an empty list which links graph types to their graph buttons
        self.graph_type_to_graph_button_id = {"temperature":[],
                                    "voltage":[],
                                    "pressure":[]}
        
        # create the buttons associated with each graph
        self.buttons = {}
        for graph in self.graphs.values():      
            btn = tk.Button(
                self.graph_type_to_frame[graph.data_type],
                text=graph.graph_id,
                command=lambda g_id=graph.graph_id, button=btn: self.show_graph(g_id, btn),
                bg="lightgray",
            )
            self.graph_type_to_graph_button[graph.data_type].append(graph.graph_id)
        
        # Configure row and column weights for resizing
        self.graph_frame_frame.grid_rowconfigure(0, weight=0)
        self.graph_frame_frame.grid_columnconfigure(1, weight=0)

        self.button_state = {}
        for button in self.buttons:
            self.button_state[button] = {self.buttons[button]:"off"}

        self.current_graph_type = None
          
    # need to fix this 
    def show_graph_buttons(self,graph_type):
        for frame in self.graph_type_to_frame.values():
            frame.pack_forget()
        for graph_t in self.graph_types.keys():
            if graph_t != graph_type:
                # i need to go through each graph of the type and turn them off
                for g in self.graph_type_to_graph_button[graph_t]:
                    self.graph_manager.hide_graph(g)                    
        self.graph_type_to_frame[graph_type].pack()

       

    def display_graph(self, graph_id, btn):
        title = btn['text']
        buttons_state = self.button_state[title]
        state = buttons_state[btn]
        print(buttons_state[btn], "current state")  

        if state == "off":
            """Placeholder for displaying the graph."""
            buttons_state[btn] = "on"
            print(buttons_state[btn], " turning on")
            self.graph_manager.show_graph(graph_id)    

        else:
            """Placeholder for displaying the graph."""
            buttons_state[btn] = "off"
            print(buttons_state[btn], " turning off")
            self.graph_manager.hide_graph(graph_id)     
            

    

