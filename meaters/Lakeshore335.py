import serial

class Lakeshore335(serial.Serial):
    def setSetpoint(self, channel:int,setpoint:float)-> None:
        """
        Summary
            Sets a setpoint
        Args:
            channel (int): channel number
            setpoint (float): setpoint
        """
        self.write(bytes(f"SETP {channel}, {setpoint}\r\n",'utf-8'))
    def setRamp(self, channel:int,on_off:int,ramp_rate:float):
        """_summary_

        Args:
            channel (int): channel
            on_off (int): if on set 1 if off set 0
            ramp_rate (float): ramping rate

        Raises:
            ValueError: when on_off parameter is not 0 or 1
        """
        if on_off == 1 or on_off ==0:
            self.write(bytes(f"RAMP {channel},{on_off},{ramp_rate}\r\n",'utf-8'))
        else:
            raise ValueError("on_off parameter must be either 1 or 0")
    def getRamp(self, channel):
        raise NotImplementedError
    def getPower(self, channel):
        raise NotImplementedError
    def getTemp(self, channel):
        raise NotImplementedError