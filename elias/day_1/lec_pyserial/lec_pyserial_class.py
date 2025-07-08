from pickletools import read_unicodestringnl

import serial
from icecream import ic
import time

ic.configureOutput(includeContext=True)
ic.disable()

class Serial:
    def __init__(self):
        self.ser = None

    ################################################
    # Open Port
    ################################################
    def openPort(self, port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False,
                   dsrdtr=False):

        # 시리얼 포트 객체 생성
        self.ser = serial.Serial()


        # 시리얼 포트설정
        self.ser.port = port             # Port Name: com1, com2,...
        self.ser.stopbits = stopbits
        self.ser.baudrate = baudrate     # Baudrate 속도: 9600, 115200, ...
        self.ser.bytesize = bytesize     # Data Bit
        self.ser.parity = parity         # Check Parity
        self.ser.timeout = timeout          # Timeout None: 무한대기, n: n초 대기
        self.ser.xonxoff = xonxoff       # Sw Flow control
        self.ser.rtscts = rtscts         # RTS/CTS Flow control
        self.ser.dsrdtr = dsrdtr         # DSR/DTR Flow control

        # 시리얼 포트 열기
        self.ser.open()

    ################################################
    # Write Port
    ################################################
    def writePort(self, data):
        return self.ser.write(data)

    def writePortUnicode(self, data, encode='utf-8'):
        return self.writePort(data.encode(encode))

    ################################################
    # Read Port
    ################################################
    def read(self, size=1, timeout=None):
        self.ser.timeout = timeout
        readed = self.ser.read(size)
        return readed

    ################################################
    # Read Line
    # Putty에서의 LineFeed값 --> Ctrl + j ('\n'
    # Enter --> Carriage Return('\r') Ctrl + m
    ################################################
    def readLine(self, timeout=None):
        self.ser.timeout = timeout
        readed = self.ser.readline()
        return readed[:-1]

    ################################################
    # Read Until ExitCode
    # Ctrl + C 값이 넘어올때까지 read
    ################################################
    def readUntilExitCode(self, code=b'\x03', timeout=None):
        self.ser.timeout = timeout
        readed = b''
        while True:
            data = self.ser.read()
            # ic(data)
            readed += data

            if data == code:
                break
        return readed[:-1]

    ################################################
    # Close Port
    ################################################
    def closePort(self):
        self.ser.close()


if __name__ == '__main__':
    # 포트열기
    ser = Serial()
    ser.openPort(port='com2')

    # 포트쓰기
    data = 'HelloWorld\r\n'
    ic(ser.writePort(data.encode())) # unicode --> bytes array
    ic(ser.writePortUnicode(data))

    # 포트읽기
    ic(ser.read(1))
    ic(ser.read(1, 5))

    # 10 byte 읽기
    ic(ser.read(10))

    # Line 읽기
    ic(ser.readLine())

    # Ctrl + C가 들어올때까지 read
    ic(ser.readUntilExitCode())

    ser.closePort()















