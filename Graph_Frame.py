import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




class Graph_Frame(tk.Frame):
    def __init__(self, graph_id, data_type, parent_frame, data_queue, colors=None, fonts=None):
        super().__init__(parent_frame)
        self.graph_id = graph_id
        self.data_type = data_type
        self.data = []
        self.state = False
        self.data_queue = data_queue
        self.colors = colors or {"bg": "gray"}  # Default if no colors provided
        self.fonts = fonts
        
        # Set up frame with consistent styling
        self.graph_frame = tk.Frame(
            parent_frame, 
            bg=self.colors.get("light_bg", "white"), 
            highlightbackground=self.colors.get("border", "gray"),
            highlightthickness=1,
            width=600, 
            height=35
        )
        
        # Set up plot with consistent styling
        self.figure, self.ax = plt.subplots(facecolor=self.colors.get("light_bg", "white"))
        self.ax.set_facecolor(self.colors.get("card_bg", "white"))
        
        # Set text colors and fonts
        title_color = self.colors.get("text_dark", "black")
        text_props = {'color': title_color}
        
        # Plot the initial line
        line_color = self.colors.get("accent", "blue")
        self.line, = self.ax.plot(self.data, label=f"Graph {graph_id}", color=line_color)

        # Style the labels, title and legend
        self.ax.legend(frameon=True, facecolor=self.colors.get("card_bg", "white"))
        self.ax.set_title(f"Graph {graph_id} - {data_type}", fontdict=text_props)
        
        # Set axis labels with consistent styling
        if data_type == "temperature":
            self.ax.set_xlabel("Time (Seconds)", fontdict=text_props)
            self.ax.set_ylabel("Temperature (Degree C)", fontdict=text_props)
            self.ax.axhline(y=30, color=self.colors.get("warning", "red"), linestyle=':', label="Min = 30")
            self.ax.axhline(y=70, color=self.colors.get("danger", "red"), linestyle=':', label="Max = 70")
        elif data_type == "pressure":
            self.ax.set_xlabel("Time (Seconds)", fontdict=text_props)
            self.ax.set_ylabel("Pressure (PSI?)", fontdict=text_props)
            self.ax.axhline(y=50, color=self.colors.get("warning", "red"), linestyle=':', label="Min = 50")
            self.ax.axhline(y=100, color=self.colors.get("danger", "red"), linestyle=':', label="Max = 100")
        elif data_type == "voltage":
            self.ax.set_xlabel("Time (Seconds)", fontdict=text_props)
            self.ax.set_ylabel("Voltage (V)", fontdict=text_props)
            self.ax.axhline(y=0, color=self.colors.get("warning", "red"), linestyle=':', label="Min = 0")
            self.ax.axhline(y=4, color=self.colors.get("danger", "red"), linestyle=':', label="Max = 4")
        
        # Style the ticks
        self.ax.tick_params(colors=title_color)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(self.colors.get("border", "gray"))
        
        self.figure.set_figheight(3)
        self.figure.set_figwidth(5.5)
        self.figure.tight_layout()
        
        # Create canvas with consistent styling
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
    
     
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