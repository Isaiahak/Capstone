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
    assert monitor_thread.safe_flag is True
    assert monitor_thread.current_error_type is None
    assert monitor_thread.last_error_type is None
    assert monitor_thread.sensor_state == "valid"
    assert monitor_thread.ejection_timer is None

def test_monitor_normal_values_high():
    q = queue.Queue()
    for _ in range(10000):      
        q.put(("test","test",random.randint(60, 90), "valid"))
    monitor_thread = Monitor_thread(q, queue.Queue(), queue.Queue(), "test", 70, 30 , "test", timer=0.1)
    for _ in range(10000):
        monitor_thread.value_analysis()
    assert monitor_thread.value_state == "unsafe"
    assert monitor_thread.safe_flag is False
    assert monitor_thread.current_error_type is "over"
    assert monitor_thread.last_error_type is "over"
    assert monitor_thread.sensor_state == "valid"
    assert monitor_thread.ejection_timer is not None

def test_monitor_normal_values_low():
    q = queue.Queue()
    for _ in range(10000):      
        q.put(("test","test",random.randint(10, 30), "valid"))
    monitor_thread = Monitor_thread(q, queue.Queue(), queue.Queue(), "test", 70, 30 , "test", timer=0.1)
    for _ in range(10000):
        monitor_thread.value_analysis()
    assert monitor_thread.value_state == "unsafe"
    assert monitor_thread.safe_flag is False
    assert monitor_thread.current_error_type is "under"
    assert monitor_thread.last_error_type is "under"
    assert monitor_thread.sensor_state == "valid"
    assert monitor_thread.ejection_timer is not None


