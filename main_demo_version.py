import pyvisa
import os
import serial
import time
from serial.tools.list_ports import comports
#################################   SET PARAMETERS HERE ###############################
stabilization_mode = True 
setponit_step = 2
mesurment_delay = 2
filename = ""
ramp_rate = 0.2
start_setpoint = 300
source_voltage = 2
end_setpoint = 70
stabilization_time = 20 #minutes
#########################################################
class qSerial(serial.Serial):
    def query(self,command:str,encoding:str = "utf-8",delay:int = 0.1) -> str:
        """_summary_

        Args:
            command (str): _description_
            encoding (str, optional): _description_. Defaults to "utf-8".
            delay (int, optional): _description_. Defaults to 0.

        Returns:
            str: _description_
        """        
        self.write(bytes(command,encoding))
        time.sleep(delay)
        return self.readline().decode()
    def available()-> None:
        """
            a function to list all available com ports
        """
        ports = comports()
        for i in ports:
            print(i) 
def main() ->None:
    global filename,start_setpoint,end_setpoint,ramp_rate,source_voltage,stabilization_mode,mesurment_delay
    mnum = 0
    Lakeshore  = qSerial.qSerial(port='COM3',baudrate=57600,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_ODD,timeout=10)
    rm = pyvisa.ResourceManager()
    kithley = rm.open_resource('USB0::0x05E6::0x2460::04452187::INSTR')
    kithley.write("OUTP ON")
    kithley.query(':MEAS:CURR?')
    kithley.write('SOUR:FUNC VOLT')
    kithley.write(f'SOUR:VOLT {source_voltage}')
    Lakeshore.write(bytes(f"SETP 1,{start_setpoint}\r\n",'utf-8'))
    time.sleep(1)
    Lakeshore.write(bytes(f"RAMP 1,1,{ramp_rate}\r\n","utf-8"))
    time.sleep(1)
    if not os.path.isfile(filename):
            datafile = open(filename , "a")
            datafile.write("Temperature A,Temperatue B,Setpoint,pwr,Current,mnumber,Time\n")
            datafile.close()
    if stabilization_mode:
        while (float(Lakeshore.query("KRDG? A\r\n")) <start_setpoint or float(Lakeshore.query("KRDG? B\r\n")) <start_setpoint):
            print(Lakeshore.query("KRDG? A\r\n"),Lakeshore.query("KRDG? A\r\n"),Lakeshore.query("KRDG?  B\r\n"),Lakeshore.query("HTR? 1\r\n"))
            time.sleep(1)
        print("temp reached")
        Setpoint = start_setpoint
        while Setpoint >= end_setpoint:
            Lakeshore.write(bytes("SETP 1,{}\r\n".format(Setpoint),'ascii'))
            time.sleep(1)
            helptime = time.time()
            while time.time() - helptime <= stabilization_time*60:
                pwr = Lakeshore.query("HTR? 1\r\n").replace("\r\n","")
                Current = str(kithley.query(':MEAS:CURR?')).replace('\n','')
                TemperatureA = float(Lakeshore.query('KRDG? A\r\n').replace("\r\n", ""))
                TemperatureB = float(Lakeshore.query('KRDG? B\r\n').replace("\r\n",""))
                msetp = Lakeshore.query("SETP?\r\n").replace("\r\n","")
                Time = round(time.time() - start_time,2)
                mnum+=1
                dataline = f"{TemperatureA},{TemperatureB},{msetp},{pwr},{Current},{mnum},{Time}\n"
                print(dataline)
                datafile = open(filename,'a')
                datafile.write(dataline)
                datafile.close()
                time.sleep(mesurment_delay)
            Setpoint -= setponit_step
        while Setpoint <= start_setpoint:
            Lakeshore.write(bytes("SETP 1,{}\r\n".format(Setpoint)))
            time.sleep(1)
            helptime = time.time()
            while time.time() - helptime <= stabilization_time*60:
                pwr = Lakeshore.query("HTR? 1\r\n").replace("\r\n","")
                Current = str(kithley.query(':MEAS:CURR?')).replace('\n','')
                TemperatureA = float(Lakeshore.query('KRDG? A\r\n').replace("\r\n", ""))
                TemperatureB = float(Lakeshore.query('KRDG? B\r\n').replace("\r\n",""))
                msetp = Lakeshore.query("SETP?\r\n").replace("\r\n","")
                Time = round(time.time() - start_time,2)
                mnum+=1
                dataline = f"{TemperatureA},{TemperatureB},{msetp},{pwr},{Current},{mnum},{Time}\n"
                print(dataline)
                datafile = open(filename,'a')
                datafile.write(dataline)
                datafile.close()
                time.sleep(mesurment_delay)
            Setpoint += setponit_step
    else:
        while (float(Lakeshore.query("KRDG? A\r\n")) <start_setpoint or float(Lakeshore.query("KRDG? B\r\n")) <start_setpoint):
            print(Lakeshore.query("KRDG? A\r\n"),Lakeshore.query("KRDG? A\r\n"),Lakeshore.query("KRDG?  B\r\n"),Lakeshore.query("HTR? 1\r\n"))
            time.sleep(1)
        print("temp reached")
        Lakeshore.write(bytes(f"SETP 1,{end_setpoint}\r\n",'utf-8'))
        TemperatureB = float(Lakeshore.query("KRDG? B\r\n").replace("\r\n",""))
        start_time = time()
    while TemperatureB > end_setpoint:
        pwr = Lakeshore.query("HTR? 1\r\n").replace("\r\n","")
        Current = str(kithley.query(':MEAS:CURR?')).replace('\n','')
        TemperatureA = float(Lakeshore.query('KRDG? A\r\n').replace("\r\n", ""))
        TemperatureB = float(Lakeshore.query('KRDG? B\r\n').replace("\r\n",""))
        msetp = Lakeshore.query("SETP?\r\n").replace("\r\n","")
        Time = round(time.time() - start_time,2)
        mnum+=1
        dataline = f"{TemperatureA},{TemperatureB},{msetp},{pwr},{Current},{mnum},{Time}\n"
        print(dataline)
        datafile = open(filename,'a')
        datafile.write(dataline)
        datafile.close()
        time.sleep(mesurment_delay)
    Lakeshore.write(bytes(f"SETP 1,{start_setpoint}\r\n",'utf-8'))
    while TemperatureB < start_setpoint:
        pwr = Lakeshore.query("HTR? 1\r\n").replace("\r\n","")
        Current = str(kithley.query(':MEAS:CURR?')).replace('\n','')
        TemperatureA = float(Lakeshore.query('KRDG? A\r\n').replace("\r\n", ""))
        TemperatureB = float(Lakeshore.query('KRDG? B\r\n').replace("\r\n",""))
        msetp = Lakeshore.query("SETP?\r\n").replace("\r\n","")
        Time = round(time.time() - start_time,2)
        mnum+=1
        dataline = f"{TemperatureA},{TemperatureB},{msetp},{pwr},{Current},{mnum},{Time}\n"
        print(dataline)
        datafile = open(filename,'a')
        datafile.write(dataline)
        datafile.close()
        time.sleep(mesurment_delay)
    Lakeshore.write(b'RANGE 1,0\r\n')
    time.sleep(1)
    Lakeshore.write(b'SETP 1, 60\r\n')
    time.sleep(1)
    Lakeshore.write(bytes(f"RAMP 1,1,0\r\n","utf-8"))
    kithley.write("OUTP OFF")
    kithley.close()
    Lakeshore.close()
if __name__ == "__main__":
    main()