class monitor:

    batteries = {"battery 1" : {"temperature" : [], "voltage": []},
                 "battery 2" : {"temperature" : [], "voltage": []},
                 "battery 3" : {"temperature" : [], "voltage": []},
                 "battery 4" : {"temperature" : [], "voltage": []}}

    def __init__(self):
        pass

    def recieveData(self,battery,dataType,data):
        # takes the value from the connector adds it to a validation queue
        pass

    def validateDate(self):
        # check the data received from the connector to see if its a value int or not then add to a queue to averaging
        pass

    def createPlotPoint(self,battery,dataType,data):
        # takes averaged value and creates a point for the graph to be plotted
        pass

    def sendAlertMessage(self,battery,dataType,data):
        # send an alert mesage to be displayed on the UI depending on the sensor value readings
        pass

    def monitoringProcess(self):
        
            

            

        
