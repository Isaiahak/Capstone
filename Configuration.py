class Configuration():
    def __new__(cls, monitor_length, error_length, ejection_time, consistent_length, temp_diff, volt_diff, timer):
        if not hasattr(cls,'instance'):
            cls.instance = super(Configuration,cls).__new__(cls)
            return cls.instance
        
    def __init__(self, monitor_length=1000, error_length=200, ejection_time=600, consistent_length=200, temp_diff=2, volt_diff=0.5, timer=0.5):
        self.monitor_length = monitor_length
        self.error_length = error_length
        self.ejection_time = ejection_time
        self.consistent_length = consistent_length
        self.temp_diff = temp_diff
        self.volt_diff = volt_diff
        self.timer = timer
        self.changed_value_flag = False 

    def get_monitor_length(self):
        return self.monitor_length

    def set_monitor_length(self, value):
        self.value_changed()
        self.monitor_length = value
        
    def get_ejection_time(self):
        return self.ejection_time

    def set_ejection_time(self, value):
        self.ejection_time = value
        
    def get_error_length(self):
        return self.error_length

    def set_error_length(self, value):
        self.value_changed()
        self.error_length = value

    def get_consistent_length(self):
        return self.consistent_length

    def set_consistent_length(self, value):
        self.value_changed()
        self.consistent_length = value

    def set_temp_diff(self, value):
        self.value_changed()
        self.temp_diff = value

    def get_temp_diff(self):
        return self.temp_diff    
        
    def set_volt_diff(self, value):
        self.value_changed()
        self.volt_diff = value
        
    def get_volt_diff(self):
        return self.volt_diff       
    
    def get_timer(self):
        return self.timer

    def set_timer(self,value):
        self.value_changed()
        self.timer = value
        
    def set_changed_flag(self):
        self.changed_value_flag = False
    
    def get_changed_flag(self):
        return self.changed_value_flag

    def value_changed(self):
        self.changed_value_flag = True


