import pytest
import queue
import random
from Monitoring_Threads import Monitor_thread


def test_monitor_normal_values():
    q = queue.Queue()
    for _ in range(10000):      
        q.put(("test","test",random.randint(30, 70), "valid"))
    monitor_thread = Monitor_thread(q, queue.Queue(), queue.Queue(), "test", 70, 30 , "test", timer=0.1)
    for _ in range(10000):
        monitor_thread.value_analysis()
    assert monitor_thread.value_state == "safe"
    assert monitor_thread.safe_flag == True
    assert monitor_thread.current_error_type == None
    assert monitor_thread.last_error_type == None
    assert monitor_thread.sensor_state == "valid"
    assert monitor_thread.ejection_timer == None

def test_monitor_high_values():
    q = queue.Queue()
    for _ in range(10000):      
        q.put(("test","test",random.randint(60, 90), "valid"))
    monitor_thread = Monitor_thread(q, queue.Queue(), queue.Queue(), "test", 70, 30 , "test", timer=0.1)
    for _ in range(10000):
        monitor_thread.value_analysis()
    assert monitor_thread.value_state == "unsafe"
    assert monitor_thread.safe_flag == False
    assert monitor_thread.current_error_type == "over"
    assert monitor_thread.last_error_type == "over"
    assert monitor_thread.sensor_state == "valid"
    assert monitor_thread.ejection_timer != None

def test_monitor_low_values():
    q = queue.Queue()
    for _ in range(10000):      
        q.put(("test","test",random.randint(10, 30), "valid"))
    monitor_thread = Monitor_thread(q, queue.Queue(), queue.Queue(), "test", 70, 30 , "test", timer=0.1)
    for _ in range(10000):
        monitor_thread.value_analysis()
    assert monitor_thread.value_state == "unsafe"
    assert monitor_thread.safe_flag == False
    assert monitor_thread.current_error_type == "under"
    assert monitor_thread.last_error_type == "under"
    assert monitor_thread.sensor_state == "valid"
    assert monitor_thread.ejection_timer != None

def test_monitor_low_and_high_values():
    q = queue.Queue()
    for _ in range(10000):      
        q.put(("test","test",random.randint(-10, 120), "valid"))
    monitor_thread = Monitor_thread(q, queue.Queue(), queue.Queue(), "test", 70, 30 , "test", timer=0.1)
    for _ in range(10000):
        monitor_thread.value_analysis()
    assert monitor_thread.value_state == "unsafe"
    assert monitor_thread.safe_flag == False
    assert monitor_thread.current_error_type == "under" or monitor_thread.current_error_type == "over"
    assert monitor_thread.last_error_type == "under" or monitor_thread.last_error_type == "over"
    assert monitor_thread.sensor_state == "valid" 
    assert monitor_thread.ejection_timer != None

def test_monitor_invalid_values():
    q = queue.Queue()
    for _ in range(10000):      
        q.put(("test","test",random.randint(30, 70), "invalid"))
    monitor_thread = Monitor_thread(q, queue.Queue(), queue.Queue(), "test", 70, 30 , "test", timer=0.1)
    for _ in range(10000):
        monitor_thread.value_analysis()
    assert monitor_thread.value_state == "unsafe"
    assert monitor_thread.safe_flag == False
    assert monitor_thread.current_error_type == "invalid"
    assert monitor_thread.last_error_type == "invalid"
    assert monitor_thread.sensor_state == "invalid"
    assert monitor_thread.ejection_timer != None

