import time 
import tkinter as tk
from tkinter import font as tkfont
import matplotlib
import os
import inspect
from Graph_Frame import Graph_Frame
matplotlib.use('TkAgg')

class UI:
    
    def __init__(self, root, temp1_graph_queue, temp2_graph_queue, temp3_graph_queue, temp4_graph_queue,notification_queue, configuration):
        # Initialize core functionality variables
        self.is_running = True
        self.configuration = configuration
        self.root = root
        self.notification_queue = notification_queue
        self.target = self.configuration
        self.frames = {}
        self.entries = {}
        self.attribute_methods = self._discover_attribute_methods()
        self.notification_list = []
        
        # Define modern color scheme
        self.colors = {
            "primary": "#2C3E50",       # Dark blue-gray for main background
            "secondary": "#34495E",     # Lighter blue-gray for secondary elements
            "accent": "#3498DB",        # Bright blue for highlights and active elements
            "accent_hover": "#2980B9",  # Darker blue for hover states
            "text": "#ECF0F1",          # Off-white for text on dark backgrounds
            "text_dark": "#2C3E50",     # Dark color for text on light backgrounds
            "success": "#2ECC71",       # Green for success messages
            "warning": "#F39C12",       # Orange for warnings
            "danger": "#E74C3C",        # Red for errors
            "light_bg": "#F5F5F5",      # Light gray for content areas
            "card_bg": "#FFFFFF",       # White for cards/elements
            "border": "#BDC3C7"         # Light gray for borders
        }
        
        # Create custom fonts
        self.fonts = {
            "header": tkfont.Font(family="Helvetica", size=14, weight="bold"),
            "subheader": tkfont.Font(family="Helvetica", size=12, weight="bold"),
            "body": tkfont.Font(family="Helvetica", size=10),
            "small": tkfont.Font(family="Helvetica", size=9),
            "button": tkfont.Font(family="Helvetica", size=10, weight="bold")
        }
        
        # Configuration details
        self.configuration_descriptions = {
            "monitor_length": "The amount of values held onto in the monitor. (400-800)",
            "error_length": "The amount of error values held onto in the monitor. (100-200)", 
            "ejection_time": "The time waited until battery ejection. (300-600 seconds)", 
            "consistent_length": "The amount of values with large differences we monitor. (100-200)",
            "temp_diff": "The difference in temperature deemed too large for normal operation. (0.5-2 degrees C)",
            "volt_diff": "The difference in voltage deemed too large for normal operation. (0.5-1 voltage)",
            "timer": "The time between value monitoring. (0.1-0.5 seconds)"
        }
        
        self.configuration_limits = {
            "monitor_length": [400, 800],                                     
            "error_length": [100, 200], 
            "ejection_time": [300, 600],                              
            "consistent_length": [100, 200],
            "temp_diff": [0.5, 2],
            "volt_diff": [0.5, 1],
            "timer": [0.1, 0.5]
        }

        # Set up root window properties
        root.configure(bg=self.colors["primary"])
        root.title("Sensor Monitoring System")
        
        # Create main frame structure with modern styling
        self.main_frame = tk.Frame(root, bg=self.colors["primary"], width=1200, height=1000)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create header with application title
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors["primary"], height=50)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.app_title = tk.Label(
            self.header_frame, 
            text="Sensor Monitoring System",
            bg=self.colors["primary"],
            fg=self.colors["text"],
            font=self.fonts["header"]
        )
        self.app_title.pack(side=tk.LEFT, padx=5)
        
        # Frame for navigation buttons
        self.buttons_frame = tk.Frame(self.main_frame, bg=self.colors["primary"], height=100)
        self.buttons_frame.pack(fill=tk.X, pady=10)
        
        # Frame for graphs
        self.graph_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["light_bg"], 
            width=1200, 
            height=600,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame for notifications
        self.notification_frame = tk.Frame(self.main_frame, bg=self.colors["light_bg"], width=1200, height=1000)
        self.notification_button_frame = tk.Frame(self.notification_frame, bg=self.colors["light_bg"], width=1200, height=100)
        self.notification_button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        # Create notification subframes
        self.ejection_notification_frame = tk.Frame(
            self.notification_frame,
            bg=self.colors["light_bg"],
            width=1200, 
            height=900,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        
        self.mosfet_notification_frame = tk.Frame(
            self.notification_frame,
            bg=self.colors["light_bg"],
            width=1200, 
            height=900,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        
        self.history_notification_frame = tk.Frame(
            self.notification_frame,
            bg=self.colors["light_bg"],
            width=1200, 
            height=900,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        
        # Add history button with modern styling
        self.create_styled_button(
            self.history_notification_frame, 
            "View History", 
            lambda: self.get_history(),
            width=20
        ).pack(side="left", pady=10,expand=True)
        
        self.text_frame = tk.Text(
            self.notification_frame, 
            bg=self.colors["light_bg"], 
            fg=self.colors["text_dark"],
            height=5, 
            width=50,
            font=self.fonts["body"]
        )

        # Frame for settings
        self.setting_frame = tk.Frame(
            self.main_frame, 
            bg=self.colors["light_bg"], 
            width=1200, 
            height=1000,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        
        # Get configuration attributes
        self.attributes = {
            attr: getattr(self.configuration, attr) 
            for attr in dir(self.configuration) 
            if not attr.startswith('_') and not callable(getattr(self.configuration, attr)) and not attr == "changed_value_flag"
        }
        
        # Create settings frames
        self.create_frames()
        
        # Navigation menu frames
        self.button_type_frame = tk.Frame(self.buttons_frame, bg=self.colors["primary"], width=1200, height=50)
        self.button_type_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Graph selection frames
        self.graph_button_frame = tk.Frame(self.buttons_frame, bg=self.colors["secondary"], width=1200, height=50)
        self.graph_button_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Create graph type selection button frames
        self.temp_button_frame = tk.Frame(self.graph_button_frame, bg=self.colors["secondary"], width=1200, height=50)
        
        # Frame for each graph type - main container for all graphs
        self.temp_graph_frame = tk.Frame(self.graph_frame, bg=self.colors["light_bg"], width=1200, height=600)
        
        # Setup graph frames
        self.temp1_graph_frame = Graph_Frame("temp1", "temperature", self.temp_graph_frame, temp1_graph_queue, self.colors, self.fonts)
        self.temp2_graph_frame = Graph_Frame("temp2", "temperature", self.temp_graph_frame, temp2_graph_queue, self.colors, self.fonts)
        self.temp3_graph_frame = Graph_Frame("temp3", "temperature", self.temp_graph_frame, temp3_graph_queue, self.colors, self.fonts)
        self.temp4_graph_frame = Graph_Frame("temp4", "temperature", self.temp_graph_frame, temp4_graph_queue, self.colors, self.fonts)

        # Structure to hold the graphs
        self.graph_map = {
            "temp1": self.temp1_graph_frame, 
            "temp2": self.temp2_graph_frame, 
            "temp3": self.temp3_graph_frame, 
            "temp4": self.temp4_graph_frame, 
        }                    
        
        self.graph_types_map = {
            "temperature": [self.temp1_graph_frame, self.temp2_graph_frame, self.temp3_graph_frame, self.temp4_graph_frame], 
        }
    
        # Structure which holds button frames
        self.graph_type_to_frame = {
            "temperature": self.temp_button_frame,
        }
        
        self.graph_type_to_graph_frame = {
            "temperature": self.temp_graph_frame,
        }
        
        # Track active graphs in order of selection
        self.active_graphs = []
        
        # Define layouts for different numbers of active graphs
        self.layouts = {
            1: [
                {"relx": 0, "rely": 0, "relwidth": 1, "relheight": 1}  # Full screen
            ],
            2: [
                {"relx": 0, "rely": 0, "relwidth": 1, "relheight": 0.5},  # Top half
                {"relx": 0, "rely": 0.5, "relwidth": 1, "relheight": 0.5}  # Bottom half
            ],
            3: [
                {"relx": 0, "rely": 0, "relwidth": 0.5, "relheight": 0.5},      # Top-left
                {"relx": 0.5, "rely": 0, "relwidth": 0.5, "relheight": 0.5},    # Top-right
                {"relx": 0, "rely": 0.5, "relwidth": 1, "relheight": 0.5}       # Bottom full
            ],
            4: [
                {"relx": 0, "rely": 0, "relwidth": 0.5, "relheight": 0.5},      # Top-left
                {"relx": 0.5, "rely": 0, "relwidth": 0.5, "relheight": 0.5},    # Top-right
                {"relx": 0, "rely": 0.5, "relwidth": 0.5, "relheight": 0.5},    # Bottom-left
                {"relx": 0.5, "rely": 0.5, "relwidth": 0.5, "relheight": 0.5}   # Bottom-right
            ]
        }

        # Generate main navigation buttons
        self.create_main_navigation()
        
        # Generate graph type buttons
        self.create_graph_type_buttons()
        
        # Generate notification buttons
        self.create_notification_buttons()
        
        # Start graph updates
        self.update_graph()
    
    def create_styled_button(self, parent, text, command, width=15, height=2, is_active=False):
        """Create a modern styled button"""
        bg_color = self.colors["accent"] if is_active else self.colors["secondary"]
        hover_color = self.colors["accent_hover"] if is_active else self.colors["accent"]
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            bg=bg_color,
            fg=self.colors["text"],
            font=self.fonts["button"],
            relief=tk.FLAT,
            borderwidth=0,
            activebackground=hover_color,
            activeforeground=self.colors["text"]
        )
        
        # Add hover effect
        button.bind("<Enter>", lambda event, btn=button, hc=hover_color: self.on_button_hover(btn, hc))
        button.bind("<Leave>", lambda event, btn=button, bc=bg_color: self.on_button_leave(btn, bc))
        
        return button
    
    def on_button_hover(self, button, hover_color):
        """Change button color on hover"""
        button.config(bg=hover_color)
    
    def on_button_leave(self, button, base_color):
        """Restore button color on leave"""
        button.config(bg=base_color)
        
    def create_main_navigation(self):
        """Create main navigation buttons"""
        # Add category buttons
        for graph_type in self.graph_type_to_frame.keys():
            icon_map = {
                "temperature": "🌡️"
            }
            icon = icon_map.get(graph_type, "")
            self.create_styled_button(
                self.button_type_frame,
                f"{icon} {graph_type.title()}",
                lambda gt=graph_type: self.show_graph_type_buttons(gt),
                width=15
            ).pack(side="left", pady=10,expand=True)
        
        self.create_styled_button(
            self.button_type_frame,
            "🔔 Alerts",
            lambda: self.show_notification_frame(),
            width=15
        ).pack(side="left", pady=10,expand=True)
        
        self.create_styled_button(
            self.button_type_frame,
            "⚙️ Settings",
            lambda: self.show_settings_frame(),
            width=15
        ).pack(side="left", pady=10,expand=True)
    
    def create_graph_type_buttons(self):
        """Create buttons for each graph"""
        for graph in self.graph_map.keys():
            if graph[0:4] == "temp":
                graph_type = "temperature"
            
            self.create_styled_button(
                self.graph_type_to_frame[graph_type],
                graph,
                lambda g=graph: self.show_graph_buttons(g),
                width=10
            ).pack(side="left", pady=5,expand=True)   
    
    def create_notification_buttons(self):
        """Create notification section buttons"""
        self.create_styled_button(
            self.notification_button_frame,
            "MOSFET Alerts",
            lambda type="mosfet": self.show_specific_notification_type(type),
            width=20
        ).pack(side="left", pady=10,expand=True)
        
        self.create_styled_button(
            self.notification_button_frame,
            "Ejection Alerts",
            lambda type="ejection": self.show_specific_notification_type(type),
            width=20
        ).pack(side="left", pady=10,expand=True)
        
        self.create_styled_button(
            self.notification_button_frame,
            "Alert History",
            lambda type="history": self.show_specific_notification_type(type),
            width=20
        ).pack(side="left", pady=10,expand=True)
    
    def _discover_attribute_methods(self):
        attribute_methods = {}
        
        # Get all methods of the target class
        methods = inspect.getmembers(self.target, predicate=inspect.ismethod)
        
        # Find getter methods (get_*, is_*, etc.) and their corresponding setters
        for name, method in methods:
            # Common getter patterns
            if name.startswith('get_'):
                attribute_name = name[4:]  # Remove 'get_' prefix
                setter_name = 'set_' + attribute_name
                
                # Check if a corresponding setter exists
                if hasattr(self.target, setter_name):
                    attribute_methods[attribute_name] = {
                        'getter': name,
                        'setter': setter_name,
                        'current_value': getattr(self.target, name)()
                    }
        return attribute_methods
        
    def update_graph(self):
        """Update all graphs and process notifications"""
        self.temp1_graph_frame.checkQueue()
        self.temp2_graph_frame.checkQueue()
        self.temp3_graph_frame.checkQueue()
        self.temp4_graph_frame.checkQueue()
        
        # Process notifications
        while not self.notification_queue.empty():
            notifications = self.notification_queue.get()
            self.notification_list.append(notifications)
            if notifications.get_notification_type() == "ejection":
                if (len(self.ejection_notification_frame.winfo_children()) > 10):
                    self.ejection_notification_frame.winfo_children()[0].destroy()
                notifications.create(self.ejection_notification_frame)
            else:
                if (len(self.mosfet_notification_frame.winfo_children()) > 10):
                    self.mosfet_notification_frame.winfo_children()[0].destroy()
                notifications.create(self.mosfet_notification_frame)
            notifications.get_frame().pack(fill=tk.X, pady=5, padx=10)
        
        # Clean up old notifications
        for notification in self.notification_list[:]:
            creation_time = notification.get_creation_time()
            if(time.time() - creation_time > 1800):
                notification.get_frame().destroy()
                self.notification_list.remove(notification)
                
        if(self.is_running):
            self.root.after(350, self.update_graph)

    def update_graph_layout(self):
        """Update the positions of all active graphs based on the active_graphs list"""
        # Get the current number of active graphs
        num_active = len(self.active_graphs)
        
        if num_active == 0:
            return
        
        # Get the layout configuration for the current number of active graphs
        # If we have more than 4 graphs, use the 4-graph layout (maximum supported)
        layout_config = self.layouts.get(min(num_active, 4), self.layouts[4])
        
        # Apply the layout to each active graph
        for i, graph_id in enumerate(self.active_graphs):
            if i >= len(layout_config):
                # If we have more graphs than layout positions, hide extra graphs
                self.graph_map[graph_id].get_frame().place_forget()
                continue
                
            position = layout_config[i]
            frame = self.graph_map[graph_id].get_frame()
            
            # Position the frame using place geometry manager
            frame.place(
                relx=position["relx"],
                rely=position["rely"],
                relwidth=position["relwidth"],
                relheight=position["relheight"]
            )

    def show_graph_buttons(self, graph): 
        """Toggle graph visibility and update layout"""
        if graph in self.active_graphs:
            # Remove graph from active list
            self.active_graphs.remove(graph)
            self.graph_map[graph].set_state(False)
            self.graph_map[graph].get_frame().place_forget()
        else:
            # Add graph to active list
            self.active_graphs.append(graph)
            self.graph_map[graph].set_state(True)
            
        # Update layout of all active graphs
        self.update_graph_layout()
            
    def show_graph_type_buttons(self, graph_type):
        """Show buttons for a specific graph type"""
        # Hide other frames
        self.notification_frame.pack_forget()
        self.setting_frame.pack_forget()
        
        # Show graph frames
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        self.graph_button_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Hide all graph type frames
        for frame in self.graph_type_to_frame.values():
            frame.pack_forget()
            
        # Reset active graphs and hide all graph frames
        self.active_graphs = []
        for graph_id, graph in self.graph_map.items():
            graph.set_state(False)
            graph.get_frame().place_forget()
            
        # Show selected graph type
        self.graph_type_to_frame[graph_type].pack(side=tk.TOP, fill=tk.X, pady=5)
        self.graph_type_to_graph_frame[graph_type].pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)

    def show_specific_notification_type(self, notification_type):
        """Show specific notification type"""
        if(notification_type == "mosfet"):
            self.ejection_notification_frame.pack_forget()
            self.history_notification_frame.pack_forget()
            self.mosfet_notification_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        elif (notification_type == "ejection"):
            self.mosfet_notification_frame.pack_forget()
            self.history_notification_frame.pack_forget()
            self.ejection_notification_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        else:
            self.mosfet_notification_frame.pack_forget()
            self.ejection_notification_frame.pack_forget()
            self.history_notification_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def get_history(self):
        """Open notification logs file"""
        os.startfile("notification_logs.csv")

    def show_notification_frame(self):
        """Show notification frames"""
        self.graph_frame.pack_forget()
        self.graph_button_frame.pack_forget()
        self.setting_frame.pack_forget()
        self.notification_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    def show_settings_frame(self):
        """Show settings frame"""
        self.graph_frame.pack_forget()
        self.graph_button_frame.pack_forget()
        self.notification_frame.pack_forget()
        self.setting_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    def end_process(self):
        """Stop the UI update process"""
        self.is_running = False
        
    def create_frames(self):
        """Create settings configuration frames"""
        # Add title to settings page
        settings_title = tk.Label(
            self.setting_frame,
            text="System Configuration",
            bg=self.colors["light_bg"],
            fg=self.colors["text_dark"],
            font=self.fonts["header"],
            pady=10
        )
        settings_title.pack(side=tk.TOP, fill=tk.X)
        canvas = tk.Canvas(
        self.setting_frame,
        bg=self.colors["light_bg"],
        highlightthickness=0
        )
        scrollbar = tk.Scrollbar(self.setting_frame, orient="vertical", command=canvas.yview)
    
        # Settings container with padding
        settings_container = tk.Frame(
            self.setting_frame,
            bg=self.colors["light_bg"],
            padx=20,
            pady=10
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_window = canvas.create_window((0, 0), window=settings_container, anchor="nw")

        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=event.width)
            canvas.itemconfig(canvas_window, width=event.width)
    
        canvas.bind('<Configure>', configure_canvas)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        settings_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        
        for i, (attr_name, methods) in enumerate(self.attribute_methods.items()):  
            if (attr_name != "changed_flag"):
                # Create a card-like frame for each setting
                card_frame = tk.Frame(
                    settings_container,
                    bg=self.colors["card_bg"],
                    highlightbackground=self.colors["border"],
                    highlightthickness=1,
                    padx=15,
                    pady=15
                )
                card_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
                
                # Setting name as header
                setting_name = tk.Label(
                    card_frame,
                    text=attr_name.replace('_', ' ').title(),
                    bg=self.colors["card_bg"],
                    fg=self.colors["text_dark"],
                    font=self.fonts["subheader"]
                )
                setting_name.pack(side=tk.TOP, anchor="w")
                
                # Setting description
                description = tk.Label(
                    card_frame,
                    text=self.configuration_descriptions[attr_name],
                    bg=self.colors["card_bg"],
                    fg=self.colors["text_dark"],
                    font=self.fonts["body"],
                    wraplength=800,
                    justify="left"
                )
                description.pack(side=tk.TOP, anchor="w", pady=(5, 10))
                
                # Input container
                input_frame = tk.Frame(card_frame, bg=self.colors["card_bg"])
                input_frame.pack(side=tk.TOP, fill=tk.X)
                
                # Text input for setting value
                input_box = tk.Text(
                    input_frame,
                    width=15,
                    height=1,
                    font=self.fonts["body"],
                    relief=tk.SOLID,
                    borderwidth=1
                )
                input_box.pack(side=tk.LEFT, padx=(0, 10))
                
                # Current value display
                current_value = getattr(self.configuration, self.attribute_methods[attr_name]['getter'])()
                current_value_label = tk.Label(
                    input_frame,
                    text=f"Current value: {current_value}",
                    bg=self.colors["card_bg"],
                    fg=self.colors["text_dark"],
                    font=self.fonts["small"]
                )
                current_value_label.pack(side=tk.LEFT, pady=5)
                
                # Save the reference to the input field
                self.frames[attr_name] = input_box
                
                # Submit button
                self.create_styled_button(
                    input_frame,
                    "Update",
                    lambda a=attr_name: self.update_numeric(a, self.frames[a].get("1.0", tk.END)),
                    width=10,
                    height=1
                ).pack(side=tk.RIGHT)
                            
    def update_numeric(self, attr_name, string_var):
        """Update numeric configuration value"""
        try:
            value = string_var.strip()
            current_value = getattr(self.target, self.attribute_methods[attr_name]['getter'])()
            value_type = type(current_value)
            
            if value_type == int:
                value = int(value)
            elif value_type == float:
                value = float(value)
                
            min_value = self.configuration_limits[attr_name][0]
            max_value = self.configuration_limits[attr_name][1]
            
            if min_value <= value <= max_value:
                self.update_attribute(attr_name, value)
            else:
                self.show_notification_popup(f"Invalid input for {attr_name}",
                                           f"Value must be between {min_value} and {max_value}")
        except ValueError:
            self.show_notification_popup("Invalid Input", f"Please enter a valid number for {attr_name}")
            
    def show_notification_popup(self, title, message):
        """Show a styled popup notification"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x150")
        popup.configure(bg=self.colors["card_bg"])
        
        # Add some padding
        frame = tk.Frame(popup, bg=self.colors["card_bg"], padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Message
        tk.Label(
            frame,
            text=message,
            bg=self.colors["card_bg"],
            fg=self.colors["text_dark"],
            font=self.fonts["body"],
            wraplength=250
        ).pack(pady=10)
        
        # OK button
        self.create_styled_button(
            frame,
            "OK",
            lambda: popup.destroy(),
            width=10,
            height=1
        ).pack(pady=10)
            
    def update_attribute(self, attr_name, value):
        """Update configuration attribute"""
        try:
            setter_method = self.attribute_methods[attr_name]['setter']
            getattr(self.target, setter_method)(value)
            
            self.show_notification_popup(
                "Setting Updated",
                f"Successfully updated {attr_name.replace('_', ' ')} to {value}"
            )
            
        except Exception as e:
            self.show_notification_popup(
                "Error",
                f"Error updating {attr_name}: {str(e)}"
            )