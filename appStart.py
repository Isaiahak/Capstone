from connector import start_server as start_connector_server
from sensorMonitor import start_server as start_monitor_server
from GUI import GraphApp
import tkinter as tk
import time
import threading
    
def start_gui():
    root = tk.Tk()
    root.title("Battery Monitor")
    root.grid_rowconfigure(0, weight=0)  # No resizing
    root.grid_columnconfigure(0, weight=0)
    root.geometry("1200x1000")  # Example: 800 pixels wide and 600 pixels tall
    root.resizable(False, False) 
    app = GraphApp(root)
    root.mainloop()
    print("started GUI")
    
    
if __name__ == "__main__":
    connector_thread = threading.Thread(target=start_connector_server)
    monitor_thread = threading.Thread(target=start_monitor_server)

    connector_thread.start()
    print("Started connector server")
    time.sleep(5)  # Sleep to allow some time for the connector server to start

    monitor_thread.start()
    print("Started Monitoring server")
    time.sleep(5)  # Sleep to allow some time for the monitor server to start

    # Start the GUI in the main thread
    start_gui()
    print("Started GUI")

    # Optionally join threads to wait for server threads to finish before the program exits
    connector_thread.join()
    monitor_thread.join()