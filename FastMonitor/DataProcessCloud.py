from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.client.sync import ModbusTcpClient as TCPClient
import uuid
import logging
import json
from datetime import datetime
from struct import *
from Models import *
from numpy import asarray
from numpy import save
from numpy import load


class DataProcessCloud(object):

    def ReadAllMeters(self, SerialPort, MeterConfig, JsonMeters):

        global MBJson
        try:
            null = None

            ArrMetConSerList = []
            ArrMetConIPList = []
            dataReaded = []

            rd = ReadData()

            '''
            for mct in MeterConfig:
                if mct["ConStatus"] == 1:
                    if mct["ComTypeId"] == 0:
                        ArrMetConSerList.append(mct)
            '''

            for mct in MeterConfig:
                if mct["ConStatus"] == 1:
                    if mct["ComTypeId"] == 1:
                        ArrMetConIPList.append(mct)

            if len(ArrMetConIPList) > 0:
                dataReaded = rd.ReadModbusTCP(MeterConfig, JsonMeters, dataReaded)

            '''
            if len(ArrMetConSerList) > 0:
                dataReaded = rd.ReadModbusSerial(SerialPort, MeterConfig, JsonMeters, dataReaded)
            '''

            return dataReaded

        except Exception as e:
            logging.info("MB Read error: %s, %s" % (e, datetime.today()))

class ReadData(object):

    def __init__(self):
        self.sdm = SaveDataModel()
        self.dt = datetime.today().replace(microsecond=0)  # Get datetime now
        self.Timestamp = int(self.dt.timestamp())  # Get Timestamp

    def ReadModbusTCP(self, MeterConfig, JsonMeters, dataReaded):

        global MBJson

        try:
            null = None

            Cnt = 0

            for mc in MeterConfig:

                client = TCPClient(mc["IPAddress"])

                if client.connect():

                    MetList = self.sdm.MeterListening(null, null, null, [])  # "ListeningDate":, "ListeningID":, "ListeningValue": {"ListeningValue":[]}, "MeterSerial": "MeterID"
                    ArrLV = []  # Array of ListeningValue for each meter(Index,Value)

                    if len(JsonMeters) > 0:
                        for Jsm in JsonMeters:
                            if Jsm[0]["model"] == mc["Models"]["ModelName"]:
                                MBJson = Jsm[0]["mbList"]
                                break

                    for mrg in mc["Models"]["MeasurRange"]:
                        if (self.dt.second % mrg["SampleTime"]) == 0:  # Determina si es momento de leer determinado rango de parámetros
                            rgM = DataF.GetRange(mrg["Range"])
                            try:
                                for rg in rgM:
                                    Ndata = (int(rg[1]) - int(rg[0])) + 1
                                    MBData = []
                                    CntDataR = 0

                                    while (Cnt < 3) and (CntDataR != Ndata):
                                        try:
                                            if mc["Models"]["MBFunctionId"] == 3:
                                                MBData = client.read_holding_registers(int(rg[0]), Ndata, unit=mc["NCPU"])
                                            elif mc["Models"]["MBFunctionId"] == 4:
                                                MBData = client.read_input_registers(int(rg[0]), Ndata, unit=mc["NCPU"])
                                            CntDataR = len(MBData.registers)
                                            Cnt += 1
                                        except Exception as e:
                                            Cnt += 1

                                    Cnt = 0

                                    if CntDataR == Ndata:
                                        ArrLV = DataF.ReadedDataToArray(self, MBData.registers, rg, ArrLV)

                            except Exception as e:
                                logging.info("Meter read error: %s, %s, %s" % (mc["MeterId"], e, datetime.today()))
                                break

                    if ArrLV:
                        if len(ArrLV) > 0:
                            '''
                            MetList["ListeningID"] = str(uuid.uuid4())
                            MetList["MeterSerial"] = mc["DeviceIdGuid"]
                            MetList["ListeningDate"] = str(self.dt)
                            MetList["listeningValue"] = ArrLV
                            dataReaded.append(MetList)
                            '''
                            data = asarray(ArrLV)
                            fileName = str(self.Timestamp) + '.npy'
                            save(fileName, data)

                if client is not None:
                    client.close()
                    del client

            return dataReaded

        except Exception as e:
            logging.info("MB Read error: %s, %s" % (e, datetime.today()))

    def ReadModbusSerial(self, SerialPort, MeterConfig, JsonMeters, dataReaded):
        global MBJson
        null = None
        client = None

        try:
            Cnt = 0
            prty = 'N'

            if SerialPort["Parity"] == 'None':
                prty = 'N'
            elif SerialPort["Parity"] == 'Even':
                prty = 'E'
            elif SerialPort["Parity"] == 'Odd':
                prty = 'O'

            client = ModbusClient(method="rtu", port=SerialPort["Port"], retries=3, stopbits=1, bytesize=8,
                                  parity=prty, baudrate=int(SerialPort["BaudRate"]), timeout=1.2)

            if client.connect():
                #For each meter
                for mc in MeterConfig:

                    MetList = self.sdm.MeterListening(null, null, null,[])  # "ListeningDate":, "ListeningID":, "ListeningValue": {"ListeningValue":[]}, "MeterSerial": "MeterID"
                    ArrLV = []  # Array of ListeningValue for each meter(Index,Value)

                    if len(JsonMeters) > 0:
                        for Jsm in JsonMeters:
                            if (Jsm[0]["model"] == mc["Models"]["ModelName"]):
                                MBJson = Jsm[0]["mbList"]
                                break

                    for mrg in mc["Models"]["MeasurRange"]:
                        if (self.dt.minute % mrg["SampleTime"]) == 0:  # Determina si es momento de leer determinado rango de parámetros
                            rgM = DataF.GetRange(mrg["Range"])
                            try:
                                for rg in rgM:
                                    Ndata = (int(rg[1]) - int(rg[0])) + 1
                                    MBData = []
                                    CntDataR = 0

                                    while (Cnt < 3) and (CntDataR != Ndata):
                                        try:
                                            if mc["Models"]["MBFunctionId"] == 3:
                                                MBData = client.read_holding_registers(int(rg[0]), Ndata,
                                                                                       unit=mc["NCPU"])
                                            elif mc["Models"]["MBFunctionId"] == 4:
                                                MBData = client.read_input_registers(int(rg[0]), Ndata, unit=mc["NCPU"])
                                            CntDataR = len(MBData.registers)
                                            Cnt += 1
                                        except Exception as e:
                                            Cnt += 1

                                    Cnt = 0

                                    if len(MBData.registers) == Ndata:
                                        ArrLV = DataF.ConvertMBData(self, mrg["MeasurTypeId"], MBData.registers,
                                                                    rg, MBJson, ArrLV)

                            except Exception as e:
                                logging.info("Meter read error: %s, %s, %s" % (mc["MeterId"], e, datetime.today()))
                                break

                    if ArrLV:
                        if len(ArrLV) > 0:
                            MetList["ListeningID"] = str(uuid.uuid4())
                            MetList["MeterSerial"] = mc["DeviceIdGuid"]
                            MetList["ListeningDate"] = str(self.dt)
                            MetList["ListeningValue"] = ArrLV
                            dataReaded.append(MetList)

            return dataReaded

        except Exception as e:
            logging.info("MB Read error: %s, %s" % (e, datetime.today()))

        finally:
            if client is not None:
                client.close()
                del client

class DataF():

    def GetRange(rg):
        rgL = rg.split(';')
        rgArr = []
        for rgV in rgL:
            rgArr.append(rgV.split(','))
        return rgArr

    def ReadedDataToArray(self, MBDataRegs, rg, MBList):
        try:
            index = int(rg[0])

            for val in MBDataRegs:
                MBList.append([index, val])
                index += 1

            return MBList
        except Exception as e:
            logging.info("ReadedDataToArray error: %s, %s" % (e, datetime.today()))

    def ConvertMBData(self, MeasureTypeId, MBDataRegs, rg, MBJson, MBList):
        try:
            null = None
            for mbrI in MBJson:
                if mbrI["MeasureTypeId"] == MeasureTypeId:
                    index = int(rg[0])
                    i = 0

                    while i < len(MBDataRegs):
                        status = False
                        j = 0
                        ind = -1
                        for l in mbrI["mbregisters"]:
                            if l["MBRegID"] == index:
                                status = True
                                ind = j
                                break
                            j = j + 1
                        if status and ind >= 0:
                            lv = self.sdm.ListeningValue(null, null)
                            if l["DataTypeId"] == 1:  # ushort
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = MBDataRegs[i] * l["Multiplier"]
                                MBList.append(lv)
                                index = index + 1
                                i = i + 1
                            elif l["DataTypeId"] == 2:  # float
                                tup = (MBDataRegs[i], MBDataRegs[i + 1])
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = unpack('>f', pack('>HH', tup[0], tup[1]))[0] * l["Multiplier"]
                                MBList.append(lv)
                                index = index + 2
                                i = i + 2
                            elif l["DataTypeId"] == 3:  # uint
                                tup = (MBDataRegs[i], MBDataRegs[i + 1])
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = unpack('>I', pack('>HH', tup[0], tup[1]))[0] * l["Multiplier"]
                                MBList.append(lv)
                                index = index + 2
                                i = i + 2
                            elif l["DataTypeId"] == 4:  # int
                                tup = (MBDataRegs[i], MBDataRegs[i + 1])
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = unpack('>i', pack('>HH', tup[0], tup[1]))[0] * l["Multiplier"]
                                MBList.append(lv)
                                index = index + 2
                                i = i + 2
                            elif l["DataTypeId"] == 5:  # ulong
                                tup = (MBDataRegs[i], MBDataRegs[i + 1], MBDataRegs[i + 2], MBDataRegs[i + 3])
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = unpack('>Q', pack('>HHHH', tup[0], tup[1], tup[2], tup[3]))[0] * l[
                                    "Multiplier"]
                                MBList.append(lv)
                                index = index + 4
                                i = i + 4
                            elif l["DataTypeId"] == 7:  # MOD10
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = MBDataRegs[i + 3] * 10E11 + MBDataRegs[i + 2] * 10E7 + MBDataRegs[
                                    i + 1] * 10E3 + MBDataRegs[i]
                                MBList.append(lv)
                                index = index + 4
                                i = i + 4
                            elif l["DataTypeId"] == 8:  # Agreagate GWh + KWh
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = MBDataRegs[i + 1] * 1E-6 + MBDataRegs[i] * 1E-3
                                MBList.append(lv)
                                index = index + 2
                                i = i + 2
                            elif l["DataTypeId"] == 9:  # double
                                tup = (MBDataRegs[i], MBDataRegs[i + 1], MBDataRegs[i + 2], MBDataRegs[i + 3])
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = unpack('>d', pack('>HHHH', tup[0], tup[1], tup[2], tup[3]))[0] * l[
                                    "Multiplier"]
                                MBList.append(lv)
                                index = index + 4
                                i = i + 4
                            elif l["DataTypeId"] == 10:  # special for PAC3200 SIEMENS
                                tup = (MBDataRegs[i], MBDataRegs[i + 1], MBDataRegs[i + 2], MBDataRegs[i + 3])
                                tup1 = (MBDataRegs[i + 4], MBDataRegs[i + 5], MBDataRegs[i + 6], MBDataRegs[i + 7])
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = ((unpack('>d', pack('>HHHH', tup[0], tup[1], tup[2], tup[3]))[0]) + (
                                    unpack('>d', pack('>HHHH', tup1[0], tup1[1], tup1[2], tup1[3]))[0])) * l[
                                                  "Multiplier"]
                                MBList.append(lv)
                                index = index + 8
                                i = i + 8
                            elif l["DataTypeId"] == 13:  # uint
                                tup = (MBDataRegs[i+1], MBDataRegs[i])
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = unpack('>I', pack('>HH', tup[0], tup[1]))[0] * l["Multiplier"]
                                MBList.append(lv)
                                index = index + 2
                                i = i + 2
                            elif l["DataTypeId"] == 11:  # int
                                tup = (MBDataRegs[i+1], MBDataRegs[i])
                                lv["Index"] = l["ParameterID"]
                                lv["Value"] = unpack('>i', pack('>HH', tup[0], tup[1]))[0] * l["Multiplier"]
                                MBList.append(lv)
                                index = index + 2
                                i = i + 2
                        else:
                            index = index + 1
                            i = i + 1

        except Exception as e:
            logging.info("Convert MB data error: %s, %s" % (e, datetime.today()))

        return MBList