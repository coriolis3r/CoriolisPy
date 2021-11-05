class SaveDataModel(object):
    def __init__(self):
        self.null = None

    def MeterListening(self, lId, mID, tst, lvArr):
        return {"ListeningId": lId, "MeterId": mID, "Timestamp": tst, "listeningvalues": lvArr}

    def ListeningValues(self, ListeningId, ParameterID, Value):
        return {"ListeningId": ListeningId, "ParameterID": ParameterID, "Value": Value}

    def ArrayOfEnergyMeter(self,mle):
        return {"Meters":mle}

    def PowerDemandValues(self,ms,arrOfEnergy):
        return {"MeterSerial":ms, "ArrayOfEnergyValue": arrOfEnergy}