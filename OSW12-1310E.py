import serial 
import numpy 
class OSW22_1310E_Switch:
    def __init__(self,sendchar= b'\n', rendchar=b'\r\n'):
        self._sendchar_ = sendchar
        self._readchar_ = rendchar
        def find_port():
            port_=None
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            for port,desc,_ in sorted(ports):
                print(f"Port: {port} -> Description: {desc}")
                if 'OSWxx' in desc:
                    port_=port
            return port_
        # if find_port() is None:
        #     raise Exception("OSW22-1310E switch not found")
        self.port = find_port()
        self.ser = serial.Serial(
            port=self.port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            rtscts=True,
            )
    def send_cmd(self,cmd):
        import sys
        try:
            cmd=cmd.encode('utf-8')+self._sendchar_
            ser=self.ser
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
        ser=self.ser
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
    def SetSwitchState(self, state):
        """
        Permissible switch state values
        1: Bar State (1<-->3, 2<-->4)
        2: Cross State (1<-->4, 2<-->3)
        """
        if state==1:
            self.send_cmd('S 1 ')
        elif state==2:
            self.send_cmd('S 2 ')
        else:
            raise ValueError("Invalid switch state. Must be 1 or 2.")

    def getSwitchState(self):
        self.send_cmd('S?')
        return self.read_return()

    
    def GetBoardType(self):
        self.send_cmd('T?')
        return self.read_return()

    def GetOSWVersion(self):
        self.send_cmd('I?')
        return self.read_return()

def main():
    # ex
    switch=OSW22_1310E_Switch()
    switch.GetOSWVersion()
    switch.getSwitchState()
    switch.SetSwitchState(1)
    switch.getSwitchState()
if __name__ == "__main__":
    main()