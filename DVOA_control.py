
class DVOA:
    def __init__(self,port,baudrate,parity,stop_bits,flow_control):
        self.port=port 
        self.baudrate=baudrate
        self.parity=parity
        self.stop_bits=stop_bits
        self.flow_control=flow_control
        self._write_termination=b'\n'
        self._read_termination=b'\r'
    def connect(self,timeout):
        """
        Create serial communication link to DVOA. 
        Timeout is time in seconds to wait for bytes to be received. Accepts floating point values ms precision.
        """
        import serial 
        import sys
        if not self.parity in serial.PARITY_NAMES.keys():
            print(f'Parity value must be one of following:{serial.PARITY_NAMES.keys()}')
        try:
            ser=serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stop_bits,
                timeout=timeout
            )
            self._ser=ser
        except Exception as exc:
            import sys
            _,_,exc_tb=sys.exc_info()
            line=exc_tb.tb_lineno
            print(f"Error: {exc} on line {line}")
    def send_cmd(self,cmd):
        """
        SUPPORTED COMMANDS: 

        PARAMETERS MUST BE SEPERATED FROM COMMAND BY SPACE. 
        """
        import sys
        try:
            cmd=cmd.encode('utf-8')+self._write_termination
            ser=self._ser
            ser.write(cmd)
            ser.flush()
        except Exception as exc:
            import sys
            _,_,exc_tb=sys.exc_info()
            line=exc_tb.tb_lineno
            print(f"Error: {exc} on line {line}")
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.close()
            print('Serial closed.')

    def read_return(self):
        import sys 
        ser=self._ser
        import time
        lines=[]
        try: 
            while True:
                time.sleep(1)
                line=ser.read_all()
                line=line.decode().strip()
                lines.append(line)
                print(line)
                time.sleep(0.1)
                if not line:
                    break
        except Exception as exc:
                _,_,exc_tb=sys.exc_info()
                line=exc_tb.tb_lineno
                print(f"Error: {exc} on line {line}")
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.close()
                print('Serial closed.')
        return lines
    def enable(self,status):
        """"
        Turn VOA on or off. 
        Status==0 : disabled
        Status ==1: enabled
        """
        self.send_cmd(f'VOA:POWer: {status}')
        self.send_cmd('VOA:POWer?')
        status=f'VOA Operational Status: {self.read_return()}'
        return status 
    def set_mode(self,mode):
        """
        mode=0,2
        0: Calibrated Attenuation
        2: Manual adjustment of voltage 
        """
        self.send_cmd(f'VOA:MODE: {mode}')
        self.read_return()
    def get_dB(self):
        """
        Get the VOA Attenuation in dB. Will return a float xx.xx dB.
        Range is based on Calibrated Attenuation Min and Max. These
        values can be acquired by sending queries of
        VOA:ATTenuation:MAX? and VOA:ATTenuation:MIN?
        """
        self.send_cmd("VOA:ATTenuation?")
        dB=self.read_return()
        return dB 
    def set_dB(self,dB):
        """
        Set VOA Attenuation in dB, xx.xx dB
        Must be in Calibrated Attenuation operating mode to set the
        Attenuation, otherwise “Err: Incorrect mode for this command”
        will be returned.
        """
        dB=float(dB)
        self.send_cmd(f"VOA:ATTenuation: {dB}")
        self.read_return()
    def restart(self):
        """
        Triggers a safe shutdown and reboots the system as a quick way
        to restore all settings to default. Returns a 1 on receipt of
        command.
        """
        self.send_cmd("SYStem:RESTART")
        self.read_return()






