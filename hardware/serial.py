import serial
import time

class Serial:
    def __init__(self, port):
        """
        port: something like '/dev/tty.usbserial-2140'
        """
        self.port = port
        self.ser = self.open_serial()

    def open_serial(self):
        return serial.Serial(
            port=self.port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )

    def start_listening(self):
        if self.ser.in_waiting:
            data = self.ser.readline()
            print(data.decode('utf-8').strip())

            time.sleep(1) # time sleep for paper goes into scanner
            return True

    def send_data(self, string):
        self.ser.write(string.encode('utf-8'))

    def destroy(self):
        self.ser.close()