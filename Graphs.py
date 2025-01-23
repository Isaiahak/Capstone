import tkinter as tk
from collections import deque
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import time
import socket
import threading

class Graph:
    def __init__(self, graph_id, data_type, initial_data):
        self.graph_id = graph_id
        self.data_type = data_type
        self.data = initial_data
        self.canvas = None
        self.canvas_widget = None
        # might need a state so i can knwo if i need to toggle on or off
        
        # Create the figure and axis
        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label=f"Graph {graph_id}")
        self.ax.legend()
        
        # Configure the graph appearance
        self.ax.set_title(f"Graph {graph_id} - {data_type}")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
    
    def update_data(self, new_data):
        self.data.append(new_data)  # Update the graph's data
        self.line.set_xdata(range(len(self.data)))  # Update the x-axis
        self.line.set_ydata(self.data)  # Update the y-axis
        self.ax.relim()  # Recompute limits
        self.ax.autoscale_view()  # Autoscale the view
    
    def render(self, parent_frame):
        # Render the graph in the provided parent frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill='both', expand=True)
        self.canvas.draw()
        
    def hide(self):
        self.canvas_widget.pack_forget()
    
class GraphManager:
    def __init__(self, parent_frame):
        self.graphs = {}  # Store graphs by ID
        self.parent_frame = parent_frame
    
    def update_graph(self, graph_id, data_type, new_data):
        if graph_id not in self.graphs:
            # Create a new graph if it doesn't exist
            self.graphs[graph_id] = Graph(graph_id, data_type, [])
            self.graphs[graph_id].render(self.parent_frame)  # Render in the frame       
        # Update the graph with new data
        self.graphs[graph_id].update_data(new_data)
        
    def hide_graph(self, graph_id):
        self.graphs[graph_id].hide()
        
    def show_graph(self, graph_id,):
        self.graphs[graph_id].render(self.parent_frame)
        
    def get_graphs(self):
        return self.graphs
        
def listen_to_socket(graph_manager):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('localhost', 8001))
    conn, addr = server_socket.accept()
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            
            if len(data) == 1:
                graph_manager.update_graph("pressure", "pressure", data)
            else:
                split_data = data.split(",")
                graph_id = int(split_data[0])
                data_type = split_data[1]
                new_data = float(split_data[2])
                graph_manager.update_graph(graph_id, data_type, new_data)
        except Exception as e:
            print(f"Error: {e}")
            break
    
    conn.close()