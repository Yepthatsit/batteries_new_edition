import pyvisa
import serial
from time import sleep
from serial.tools.list_ports import comports
#################################   SET PARAMETERS HERE ###############################
stabilization_mode = True 


filename = ""
ramp_rate = 0.2
start_setpoint = 300
source_voltage = 2
end_setpoint = 70


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
        sleep(delay)
        return self.readline().decode()
    def available()-> None:
        """
            a function to list all available com ports
        """
        ports = comports()
        for i in ports:
            print(i) 
def main() ->None:
    global filename,start_setpoint,end_setpoint,ramp_rate,source_voltage,stabilization_mode
    Lakeshore  = qSerial.qSerial(port='COM3',baudrate=57600,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_ODD,timeout=10)
    rm = pyvisa.ResourceManager()
    kithley = rm.open_resource('USB0::0x05E6::0x2460::04452187::INSTR')
    kithley.write("OUTP ON")
    kithley.query(':MEAS:CURR?')
    kithley.write('SOUR:FUNC VOLT')
    kithley.write(f'SOUR:VOLT {source_voltage}')
    Lakeshore.write(bytes(f"RAMP 1,1,{ramp_rate}\r\n","utf-8"))
    sleep(1)
    if stabilization_mode:
        pass
    else:
        raise NotImplementedError
if __name__ == "__main__":
    main()