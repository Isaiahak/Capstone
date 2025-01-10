import tkinter as tk
from collections import deque
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import time

class RollingGraph:
    def __init__(self, master, max_points=300, title="Rolling Graph", ylabel="Temperature (°C)"):
        """Initialize the rolling graph."""
        self.master = master
        self.max_points = max_points

        # Rolling data storage
        self.x_data = deque(maxlen=max_points)  # Time values
        self.y_data = deque(maxlen=max_points)  # Temperature values

        # Initialize with some data
        current_time = time.time()
        for i in range(max_points):
            self.x_data.append(current_time + i - max_points)  # Past timestamps
            self.y_data.append(random.uniform(20, 30))  # Simulated temperatures

        # Create Matplotlib figure
        self.figure = Figure(figsize=(4, 2), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.line, = self.ax.plot(self.x_data, self.y_data, color="blue", label="Temperature")
        self.ax.set_title(title)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel(ylabel)
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)

        # Start updating the graph
        self.update_graph()

    def update_graph(self):
        """Update the graph with new data."""
        current_time = time.time()
        # figure out how to get this be the data from the micro controller
        new_temperature = random.uniform(20, 30)  # Simulate temperature

        # Append new data
        self.x_data.append(current_time)
        self.y_data.append(new_temperature)

        # Update the plot
        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()

        # Redraw the canvas
        self.canvas.draw()

        # Schedule the next update
        self.master.after(100, self.update_graph)  # Update every 100 ms


    def show_graph(self):
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
    
    def hide_graph(self):
        self.canvas.get_tk_widget().pack_forget() 

    
