class Configuration():
    def __new__(cls, monitor_length, error_length, ejection_time):
        if not hasattr(cls,'instance'):
            cls.instance = super(Configuration,cls).__new__(cls)
            return cls.instance
        
    def __init__(self, monitor_length=1000, error_length=200, ejection_time=600):
        self.monitor_length = monitor_length
        self.error_length = error_length
        self.ejection_time = ejection_time

    def get_monitor_length(self):
        return self.monitor_length

    def set_monitor_length(self, value):
        self.monitor_length = value
        
    def get_ejection_time(self):
        return self.ejection_time

    def set_ejection_time(self, value):
        self.ejection_time = value
        
    def get_error_length(self):
        return self.error_length

    def set_error_length(self, value):
        self.error_length = value
        
        
            
    