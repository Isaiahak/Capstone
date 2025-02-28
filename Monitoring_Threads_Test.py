import pytest
import queue
import random
from Monitoring_Threads import Monitor_thread


@pytest.fixture
# function for creating queues
def create_queue(name, data, state):
    q = queue.Queue()
    for _ in range(1000):      
        q.put("test",name,data,state)
    return q

#temperature queue
@pytest.fixture
def input_queue():
    return create_queue("test",random.randint(30, 70), "valid")


#temperature monitor for normal temperature
@pytest.fixture
def monitor_thread():
    return  Monitor_thread(input_queue, queue.Queue(), queue.Queue(), "test", 70, 30 , "test", timer=0.1)

def test_monitor(monitor_thread):
    while monitor_thread.queue.qsize() > 0:
         monitor_thread.value_analysis()
    assert monitor_thread.value_state == "safe"
    assert monitor_thread.safe_flag is True
    assert monitor_thread.current_error_type is None
    assert monitor_thread.last_error_type is None
    assert monitor_thread.sensor_state == "valid"
    assert monitor_thread.ejection_timer is None


