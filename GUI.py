import tkinter as tk
from Graphs import RollingGraph

class GraphApp:
    def __init__(self, root):
        #graph buttons frame 
        self.graph_frame_frame = tk.Frame(root, bg="white", width=800,height=100)
        self.graph_frame_frame.pack_propagate(False)
        self.graph_frame_frame.pack()

        # Initialize data
        self.graph_types = {
            "Temperature": ["Temp 1", "Temp 2", "Temp 3", "Temp 4"],
            "Voltage": ["Volt 1", "Volt 2", "Volt 3", "Volt 4"],
            "Pressure": ["Press 1"],
        }

        #graph type button frame
        self.graph_type_frame = tk.Frame(self.graph_frame_frame)
        self.graph_type_frame.pack()
        
        self.type_buttons = {}
        #graph type buttons
        for graph_type in self.graph_types.keys():
            btn = tk.Button(
                self.graph_type_frame,
                text=graph_type,
                command=lambda g_type=graph_type: self.show_graph_buttons(g_type),
                bg="lightgray",
            )
            btn.pack(side="left", pady=10, padx=10, fill="x")
            self.type_buttons[graph_type] = btn 

        #graph selection button frame
        self.temp_button_frame = tk.Frame(self.graph_frame_frame, bg="blue", width=800, height=100)

        self.volt_button_frame = tk.Frame(self.graph_frame_frame, bg="blue", width=800, height=100)
       
        self.press_button_frame = tk.Frame(self.graph_frame_frame, bg="blue", width=800, height=100)

        self.graph_type_to_frame = {"Temperature":self.temp_button_frame,
                                    "Voltage":self.volt_button_frame,
                                    "Pressure":self.press_button_frame}
        
        temperature_1 = RollingGraph(master=root, title="Temp 1", ylabel="Temperature (°C)")
        temperature_2 = RollingGraph(master=root, title="Temp 2", ylabel="Temperature (°C)")
        temperature_3 = RollingGraph(master=root, title="Temp 3", ylabel="Temperature (°C)")
        temperature_4 = RollingGraph(master=root, title="Temp 4", ylabel="Temperature (°C)")

        voltage_1 = RollingGraph(master=root, title="Volt 1", ylabel="Voltage (V)")
        voltage_2 = RollingGraph(master=root, title="Volt 2", ylabel="Voltage (V)")
        voltage_3 = RollingGraph(master=root, title="Volt 3", ylabel="Voltage (V)") 
        voltage_4 = RollingGraph(master=root, title="Volt 4", ylabel="Voltage (V)")

        #if we are doing a pressure sensor figure out the units 
        pressure = RollingGraph(master=root, title="Press 1", ylabel="PSI ?? (°C)")

        #name of graph and graph object dict
        self.name_to_graph = {"Temp 1":temperature_1,
                         "Temp 2":temperature_2,
                         "Temp 3":temperature_3,
                         "Temp 4":temperature_4,
                         "Volt 1":voltage_1,
                         "Volt 2":voltage_2,
                         "Volt 3":voltage_3,
                         "Volt 4":voltage_4,
                         "Press 1":pressure}

        self.buttons = {}

        graphs = self.graph_types.keys()
        for graph_type in graphs:
            for graph in self.graph_types[graph_type]:
                btn = tk.Button(
                    self.graph_type_to_frame[graph_type],
                    text=graph,
                    bg="lightgray",
                    state="normal"
                )
                btn.config(command=lambda g=self.name_to_graph[graph], b=btn: self.display_graph(g,b))
                btn.pack(side="left", pady=10, padx=10, fill="x") 
                self.buttons[graph] = btn 

        self.graph_type_to_graph_button = {}
        # bind all of the type buttons to their set of graph buttons
        for type in self.type_buttons.keys():
            buttons = self.graph_types[type]
            self.graph_type_to_graph_button[type] = buttons

        # Configure row and column weights for resizing
        self.graph_frame_frame.grid_rowconfigure(0, weight=0)
        self.graph_frame_frame.grid_columnconfigure(1, weight=0)

        self.button_state = {}
        for button in self.buttons:
            self.button_state[button] = {self.buttons[button]:"off"}

        self.current_graph_type = None

    def show_graph_buttons(self,graph_type):
        for frame in self.graph_type_to_frame.values():
            frame.pack_forget()
        for graph_t in self.graph_types:
            if graph_t != graph_type:
                for g in self.graph_types[graph_t]:
                    graph = self.name_to_graph[g]  
                    graph.hide_graph()
        self.graph_type_to_frame[graph_type].pack()

       

    def display_graph(self, graph, btn):
        title = btn['text']
        buttons_state = self.button_state[title]
        state = buttons_state[btn]
        print(buttons_state[btn], "current state")  

        if state == "off":
            """Placeholder for displaying the graph."""
            buttons_state[btn] = "on"
            print(buttons_state[btn], " turning on")
            graph.show_graph()    

        else:
            """Placeholder for displaying the graph."""
            buttons_state[btn] = "off"
            print(buttons_state[btn], " turning off")
            graph.hide_graph()     
            

    

# Main application
root = tk.Tk()
root.title("Battery Monitor")
root.grid_rowconfigure(0, weight=0)  # No resizing
root.grid_columnconfigure(0, weight=0)
root.geometry("1200x1000")  # Example: 800 pixels wide and 600 pixels tall
root.resizable(False, False) 
app = GraphApp(root)
root.mainloop()

