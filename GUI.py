import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time

class TemperatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Monitoring GUI")

        # Graph management
        self.graphs = {}  # Store graphs as {name: data}
        self.time_data = []  # Shared time data for all graphs
        self.graph_names = ["Graph A", "Graph B", "Graph C", "Graph D"]  # Predefined graph names

        # UI Components
        self.create_controls()
        self.create_graph_frames()

        # Start updating temperature values
        self.update_temperature()

    def create_controls(self):
        """Create the control panel with buttons and dropdowns."""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        # Dropdown for adding graphs
        self.add_graph_var = tk.StringVar(value=self.graph_names[0])
        ttk.Label(control_frame, text="Add Graph:").grid(row=0, column=0, padx=5)
        self.add_dropdown = ttk.OptionMenu(control_frame, self.add_graph_var, *self.graph_names)
        self.add_dropdown.grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Add", command=self.add_graph).grid(row=0, column=2, padx=5)

        # Dropdown for removing graphs
        self.remove_graph_var = tk.StringVar(value="")
        ttk.Label(control_frame, text="Remove Graph:").grid(row=1, column=0, padx=5)
        self.remove_dropdown = ttk.OptionMenu(control_frame, self.remove_graph_var, "")
        self.remove_dropdown.grid(row=1, column=1, padx=5)
        ttk.Button(control_frame, text="Remove", command=self.remove_graph).grid(row=1, column=2, padx=5)

    def create_graph_frames(self):
        """Create frames for displaying graphs."""
        self.graph_frames = []
        self.update_graph_layout()

    def update_graph_layout(self):
        """Update the layout to display the current graphs."""
        # Remove old frames
        for _, frame in self.graph_frames:  # Unpack the tuple to access the frame
            frame.destroy()

        self.graph_frames = []

        # Create new frames for each graph
        for name in self.graphs:
            frame = ttk.Frame(self.root)
            frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
            self.graph_frames.append((name, frame))

        # Update the removal dropdown menu
        self.update_remove_dropdown()

        # Draw the graphs
        self.draw_graphs()

    def draw_graphs(self):
        """Draw graphs in the current frames."""
        for name, frame in self.graph_frames:
            for widget in frame.winfo_children():
                widget.destroy()  # Clear the frame

            # Create a Matplotlib figure for temperature plot
            fig = Figure(figsize=(4, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_title(f"{name} - Temperature")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Temperature (°C)")

            # Plot the temperature data
            if len(self.time_data) > 0 and len(self.graphs[name]) > 0:
                ax.plot(self.time_data, self.graphs[name], color="blue", label="Temperature")
                ax.legend()

            # Add the canvas to the frame
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def add_graph(self):
        """Add a new graph based on the selected name."""
        graph_name = self.add_graph_var.get()

        if graph_name not in self.graphs:
            self.graphs[graph_name] = []  # Initialize graph data
            self.update_graph_layout()
        else:
            print(f"Graph {graph_name} already exists.")

    def remove_graph(self):
        """Remove the selected graph."""
        graph_name = self.remove_graph_var.get()

        if graph_name in self.graphs:
            del self.graphs[graph_name]  # Remove the graph data
            self.update_graph_layout()
        else:
            print(f"Graph {graph_name} does not exist.")

    def update_remove_dropdown(self):
        """Update the options in the remove dropdown."""
        menu = self.remove_dropdown["menu"]
        menu.delete(0, "end")  # Clear current options
        for name in self.graphs.keys():
            menu.add_command(label=name, command=lambda value=name: self.remove_graph_var.set(value))

    def update_temperature(self):
        """Simulate real-time temperature updates."""
        current_time = time.time()  # Get the current time in seconds

        if len(self.time_data) == 0 or current_time - self.time_data[-1] >= 1:
            # Append the time if at least 1 second has passed
            self.time_data.append(current_time if len(self.time_data) == 0 else self.time_data[-1] + 1)

            # Update each graph with random temperature values (simulate real readings)
            for name in self.graphs:
                self.graphs[name].append(random.uniform(20, 30))  # Simulate temperature values between 20-30°C

                # Trim temperature data to match the length of time_data
                while len(self.graphs[name]) > len(self.time_data):
                    self.graphs[name].pop(0)

            # Trim time data to match the length of the shortest graph
            min_length = min(len(data) for data in self.graphs.values()) if self.graphs else len(self.time_data)
            self.time_data = self.time_data[-min_length:]

        # Redraw the graphs
        self.draw_graphs()

        # Schedule the next update
        self.root.after(1000, self.update_temperature)



# Run the application
root = tk.Tk()
app = TemperatureApp(root)
root.mainloop()
