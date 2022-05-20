class SaveDataModel(object):
    def __init__(self):
        self.null = None

    def MeterListening(self, lId, mID, tst, lvArr):
        return {"id": lId, "MeterId": mID, "ListeningDate": tst, "ListeningValue": lvArr}

    def ListeningValue(self, lid, pid, Value):
        return {"id": lid, "ParameterId": pid, "Value": Value}

    def ArrayOfEnergyMeter(self,mle):
        return {"Meters":mle}

    def PowerDemandValues(self,ms,arrOfEnergy):
        return {"MeterSerial":ms, "ArrayOfEnergyValue": arrOfEnergy}