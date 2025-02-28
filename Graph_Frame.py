import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph_Frame(tk.Frame):
    def __init__(self, graph_id, data_type, parent_frame, data_queue):
        super().__init__(parent_frame)
        self.graph_id = graph_id
        self.data_type = data_type
        self.data = [] # might have  a backup csv
        self.state = False
        self.data_queue = data_queue
        self.graph_frame = tk.Frame(parent_frame, bg="gray", width=600, height=35)
        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.data, label=f"Graph {graph_id}")
        self.ax.legend()
        self.ax.set_title(f"Graph {graph_id} - {data_type}")
        if ( data_type == "temperature"):
            self.ax.set_xlabel("Time ( Seconds)")
            self.ax.set_ylabel("Temperature (Degree C)") 
            self.ax.axhline(y=30, color='red', linestyle=':', label=f"Min = 30")
            self.ax.axhline(y=70, color='red', linestyle=':', label=f"Max = 70")
        if ( data_type == "pressure"):
            self.ax.set_xlabel("Time ( Seconds)")
            self.ax.set_ylabel("Pressure (PSI?)") 
            self.ax.axhline(y=50, color='red', linestyle=':', label=f"Min = 50")
            self.ax.axhline(y=100, color='red', linestyle=':', label=f"Max = 100")
        if ( data_type == "voltage"):
            self.ax.set_xlabel("Time ( Seconds)")
            self.ax.set_ylabel("Voltage (V)") 
            self.ax.axhline(y=0, color='red', linestyle=':', label=f"Min = 0")
            self.ax.axhline(y=4, color='red', linestyle=':', label=f"Max = 4")
        self.figure.set_figheight(3)
        self.figure.set_figwidth(5.5)
        self.figure.tight_layout()
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