class SaveDataModel(object):
    def __init__(self):
        self.null = None

    def MeterListening(self, lId, ms, ld, lvArr):
        #ListeningValue: [{"Index":null,"Value":null},{"Index":null,"Value":null}...]
        return {"ListeningID": lId, "MeterSerial": ms, "ListeningDate": ld, "ListeningValue": lvArr}

    def ListeningValue(self, Index, Value):
        return {"Index": Index, "Value": Value}

    def ArrayOfEnergyMeter(self,mle):
        return {"Meters":mle}

    def PowerDemandValues(self,ms,arrOfEnergy):
        return {"MeterSerial":ms, "ArrayOfEnergyValue": arrOfEnergy}