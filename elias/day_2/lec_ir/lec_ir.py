import ctypes

# https://www.redrat.co.uk/
# https://gist.github.com/kevroy314/066f49f0b346e2ab898d91423b94da48
# Copyright 2010 Ben Smith (benjamin.coder.smith@gmail.com)
# Used to access hardware features on the USB-UIRT device http://www.usbuirt.com
# relies on the uuirtdrv.so library and USB-UIRT hardware device
# Public Domain.

DEFAULT_UUIRTDRV_LIBRARY_LOCATION = "./uuirtdrv.dll"

PUUCALLBACKPROC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_void_p)
PLEARNCALLBACKPROC = ctypes.CFUNCTYPE(None, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes.c_void_p)

OPENEX_ATTRIBUTE_EXCLUSIVE = 0x0001

ERR_NO_DEVICE = 0x20000001
ERR_NO_RESP = 0x20000002
ERR_NO_DLL = 0x20000003
ERR_VERSION = 0x20000004
ERR_IN_USE = 0x20000005

CFG_LEDRX = 0x0001
CFG_LEDTX = 0x0002
CFG_LEGACYRX = 0x0004

IRFMT_UUIRT = 0x0000
IRFMT_PRONTO = 0x0010

IRFMT_LEARN_FORCERAW = 0x0100
IRFMT_LEARN_FORCESTRUC = 0x0200
IRFMT_LEARN_FORCEFREQ = 0x0400
IRFMT_LEARN_FREQDETECT = 0x0800
IRFMT_LEARN_UIR = 0x4000
IRFMT_LEARN_DEBUG = 0x8000
IRFMT_TRANSMIT_DC = 0x0080

# Normal
BIT_1 = "1640"
BIT_0 = "1615"

# Factory
F_BIT_1 = "1540"
F_BIT_0 = "1515"

# LG Remote Controller
class IrCodes:
    KEY_POWER = '08'
    KEY_MONITOR_ON = 'c4'
    KEY_MONITOR_OFF = 'c5'
    KEY_ENERGY_SAVING = '95'
    KEY_INPUT = '0b'
    KEY_NUM0 = '10'
    KEY_NUM1 = '11'
    KEY_NUM2 = '12'
    KEY_NUM3 = '13'
    KEY_NUM4 = '14'
    KEY_NUM5 = '15'
    KEY_NUM6 = '16'
    KEY_NUM7 = '17'
    KEY_NUM8 = '18'
    KEY_NUM9 = '19'
    KEY_CH_UP = '00'
    KEY_CH_DOWN = '01'
    KEY_VOL_UP = '02'
    KEY_VOL_DOWN = '03'
    KEY_BRIGHTNESS_UP = 'e0'
    KEY_BRIGHTNESS_DOWN = 'e1'
    KEY_3D = 'dc'
    KEY_1_a_A = '32'
    KEY_CLEAR = '2f'
    KEY_SIMPLINK = '7e'
    KEY_ARC = '79'
    KEY_PSM = '4d'
    KEY_MUTE = '09'
    KEY_SETTINGS = '43'
    KEY_AUTO_CONFIG = '99'
    KEY_UP = '40'
    KEY_DOWN = '41'
    KEY_RIGHT = '06'
    KEY_LEFT = '07'
    KEY_OK = '44'
    KEY_BACK = '28'
    KEY_TILE = '7b'
    KEY_EXIT = '5b'
    KEY_ID_ON = '72'
    KEY_ID_OFF = '71'
    KEY_YELLOW = '63'
    KEY_BLUE = '61'
    KEY_STOP = 'b1'
    KEY_PLAY = 'b0'
    KEY_PAUSE = 'ba'
    KEY_BACKWARD = '8f'
    KEY_FORWARD = '8e'
    KEY_W_BAL = '5f'
    KEY_S_MENU = '3f'
    KEY_HOME = '7c'
    KEY_SWAP = '97'
    KEY_MIRROR = '96'
    KEY_INSTART = 'fb'
    KEY_INSTOP = 'fa'
    KEY_ADJ = 'ff'


class IrCodes_BlackBoard:
    KEY_POWER = '52'
    KEY_OK = '4a'
    KEY_LEFT = '49'
    KEY_RIGHT = '4b'
    KEY_UP = '47'
    KEY_DOWN = '4d'
    KEY_INPUT = '07'
    KEY_DISPLAY = '1c'


class UUINFO(ctypes.Structure):
    """wraps uuinfo struct"""
    _fields_ = [("fwVersion", ctypes.c_uint),
                ("protVersion", ctypes.c_uint),
                ("fwDateDay", ctypes.c_ubyte),
                ("fwDateMonth", ctypes.c_ubyte),
                ("fwDateYear", ctypes.c_ubyte)
                ]


class UUGPIO(ctypes.Structure):
    """wraps uugpio struct"""
    _fields_ = [("irCode", ctypes.c_ubyte * 6),
                ("action", ctypes.c_ubyte),
                ("duration", ctypes.c_ubyte)
                ]


class UsbUirt:
    LG_REMOTE = 0
    E_BLACK_BOARD_REMOTE = 1
    PANASONIC = 2
    """Wraps the USB-UIRT C API for Python."""

    def __init__(self, library_location=DEFAULT_UUIRTDRV_LIBRARY_LOCATION):
        """Accepts a path to uuirtdrv.so - probably has to be changed a little for windows"""
        uuirtlib = ctypes.windll.LoadLibrary(library_location)
        self.__UUIRTOpen = uuirtlib.UUIRTOpen
        self.__UUIRTOpenEx = uuirtlib.UUIRTOpenEx
        self.__UUIRTClose = uuirtlib.UUIRTClose
        self.__UUIRTGetDrvInfo = uuirtlib.UUIRTGetDrvInfo
        self.__UUIRTGetDrvVersion = uuirtlib.UUIRTGetDrvVersion
        self.__UUIRTGetUUIRTInfo = uuirtlib.UUIRTGetUUIRTInfo
        self.__UUIRTGetUUIRTConfig = uuirtlib.UUIRTGetUUIRTConfig
        self.__UUIRTSetUUIRTConfig = uuirtlib.UUIRTSetUUIRTConfig
        self.__UUIRTTransmitIR = uuirtlib.UUIRTTransmitIR
        self.__UUIRTLearnIR = uuirtlib.UUIRTLearnIR
        self.__UUIRTSetReceiveCallback = uuirtlib.UUIRTSetReceiveCallback
        self.__UUIRTGetUUIRTGPIOCfg = uuirtlib.UUIRTGetUUIRTGPIOCfg
        self.__UUIRTSetUUIRTGPIOCfg = uuirtlib.UUIRTSetUUIRTGPIOCfg
        self.__dev_handle = ctypes.c_void_p()
        self.__opened = False
        self.__receiveCallback = None
        self.__learnCallback = None
        self.__receiveUserData = None
        self.__receiveUserDataType = None
        self.__learnUserData = None
        self.__learnUserDataType = None

        # Python 2.6 and later - not sure what to wrap this with on earlier versions
        self.__abort = ctypes.c_bool(False)

    def _receiveCallback(self, codeID, userdata):
        """Translates codeID and userdata from ctypes to python objects."""
        data = None
        if (userdata):
            data = ctypes.py_object.from_address(userdata).value
        self.receiveCallback(bytes(codeID), data)

    def _learnCallback(self, progress, signalQuality, carrierFrequency, userdata):
        """Translates parameters from ctypes to python"""
        data = None
        if (userdata):
            data = ctypes.py_object.from_address(userdata).value
        self.learnCallback(int(progress.value), int(signalQuality.value), int(carrierFrequency.value), data)

    def receiveCallback(self, codeID, userdata):
        """Override this function to intercept IR code identifiers."""
        print(codeID, userdata)

    def learnCallback(self, progress, signalQuality, carrierFrequency, userdata):
        """Implement this function for progress reports for IR learning."""
        print(progress, signalQuality, carrierFrequency, userdata)

    def open(self, userdata=None):
        """Open the USB UIRT device.  Can throw exceptions."""
        if not self.__opened:
            self.__dev_handle = ctypes.c_void_p(self.__UUIRTOpen())
            if self.__dev_handle:
                self.__opened = True
            else:
                raise IOError

    #             rv = self.setReceiveCallback(self._receiveCallback, userdata)
    #             if (rv == 0):
    #                 raise Exception

    def __del__(self):
        """Close device on destroy."""
        if self.__opened:
            self.__UUIRTClose(self.__dev_handle)

    def close(self):
        """Close the device."""
        if self.__opened:
            # throw on error. whatcha gonna do
            rv = self.__UUIRTClose(self.__dev_handle)
            if rv == 0:
                raise Exception
            self.__opened = False

    def getDrvInfo(self):
        """Wraps UUIRTGetDrvInfo, returns Python int().  This function may be called before self.open()."""
        version = ctypes.c_uint()
        rv = self.__UUIRTGetDrvInfo(ctypes.byref(version))
        if rv == 0:
            raise Exception
        return version.value

    def getDrvVersion(self):
        """Wraps UUIRTGetDrvVersion, returns Python int()"""
        if not self.__opened:
            raise Exception
        version = ctypes.c_uint()
        rv = self.__UUIRTGetDrvVersion(ctypes.byref(version))
        if rv == 0:
            raise Exception
        return version.value

    def getUUIRTInfo(self):
        """Wraps UUIRTGetUUIRTInfo, returns usbuirt.UUINFO()."""
        if not self.__opened:
            raise Exception
        info = UUINFO()
        rv = self.__UUIRTGetUUIRTInfo(self.__dev_handle, ctypes.byref(info))
        if rv == 0:
            raise Exception
        return info

    def getUUIRTConfig(self):
        """Wraps UUIRTGetUUIRTConfig, returns Python int()."""
        if not self.__opened:
            raise Exception
        cfg = ctypes.c_uint32()
        puconfig = ctypes.byref(ctypes.c_uint32())
        rv = self.__UUIRTGetUUIRTConfig(self.__dev_handle, ctypes.byref(cfg))
        if rv == 0:
            raise Exception
        return cfg.value

    def setUUIRTConfig(self, config):
        """Wraps UUIRTSetUUIRTConfig, config is an int()."""
        if not self.__opened:
            raise Exception
        uconfig = ctypes.c_uint32(config)
        return (self.__UUIRTSetUUIRTConfig(self.__dev_handle, uconfig) == 1)

    def transmitIR(self, ircode, codeformat, repeatcount, inactivitywaittime):
        """Wraps UUIRTTransmitIR, ircode is a str(), other parameters are int()."""
        if not self.__opened:
            raise Exception
        # code = ctypes.c_char_p(ircode)
        code = ctypes.cast(ircode, ctypes.c_char_p)
        # print code
        return (self.__UUIRTTransmitIR(self.__dev_handle, code, codeformat, repeatcount, inactivitywaittime, None, None,
                                       None) == 1)

    def changSignalBitToHexString(self, signalBit):
        print(signalBit)
        headCode = signalBit[0:16]  # 앞에서 부터 16byte
        signals = signalBit[16:(4 * 8 * 4) + 16]  # 16 바이트 부터 32byte
        stdValue = signalBit[16 + (4 * 8 * 4):16 + (4 * 8 * 4) + 2]
        print(stdValue)
        print(signals)
        stdValue = int(stdValue) * 100 + 30  # 0,1을 구분하는 기준값
        bitString = ''
        index = 0
        for i in range(0, 32):
            bit = int(signals[index:index + 4])
            print(bit)
            if bit > stdValue:
                bitString += '1'
            else:
                bitString += '0'
            index += 4
        print(bitString)
        irCode = bitString[16:16 + 8]  # Front 16: Address, 8: Command, 8: Reverse Command
        print(irCode)
        irCode = irCode[::-1]  # big endian -> little endian
        print(irCode)
        print(hex(int(irCode, 2)))
        irCode = hex(int(irCode, 2))[2:4]
        return headCode, stdValue, irCode

    # https://exploreembedded.com/wiki/NEC_IR_Remote_Control_Interface_with_8051

    def learnIR(self, codeformat, callback, userdata, abort, param1):
        """Wraps UUIRTLearnIR, returns a list of int().
            codeformat is an int(),
            callback is a Python ctypes function usbuirt.PLEARNCALLBACKPROC(),
            userdata is any python object and will be sent to the callback function,
            abort is a boolean, and should be set to false - and theoretically setting it to true will interrupt the learning process
            param1 should be 0 unless there's a good reason according to the docs
            Note that changing this callback will override self.learnCallback and self._learnCallback."""
        # ircode create_string_buffer
        if not self.__opened:
            raise Exception
        buff = ctypes.create_string_buffer(4096)
        if callback:
            self.__learnCallback = PLEARNCALLBACKPROC(callback)

        # Python 2.6 and later.
        self.__abort = ctypes.c_bool(abort)
        self.__learnUserData = userdata
        # the type needs a reference count retained to reconstruct
        self.__learnUserDataType = ctypes.py_object(self.__learnUserData)
        rv = self.__UUIRTLearnIR(self.__dev_handle,
                                 ctypes.c_int(codeformat),
                                 ctypes.byref(buff),
                                 self.__learnCallback,
                                 ctypes.cast(ctypes.addressof(self.__learnUserDataType), ctypes.c_void_p),
                                 ctypes.byref(self.__abort),
                                 param1, None, None)
        if rv == 0:
            raise Exception
        # vals = [int(x, 16) for x in buff.value.split(' ')]
        vals = ""
        # for x in buff.value.split(' '):
        #    vals += x
        #         return vals
        print('1')
        print(buff.value)
        return self.changSignalBitToHexString(buff.value)

    #         return buff.value

    def setReceiveCallback(self, callback, userdata):
        """Wrap UUIRTSetReceiveCallback, callback is of type PUUCALLBACKPROC(), userdata is any python object and will be sent to the callback.
            Note that changing this callback will override self.receiveCallback and self._receiveCallback."""
        if not self.__opened:
            raise Exception
        if callback:
            self.__receiveCallback = PUUCALLBACKPROC(callback)
        self.__receiveUserData = userdata

        # retaining a reference to this type seems necessary to reconstruct.
        # Honestly it would have been easier to keep userdata in the instance and pass None into
        # the callback, but I wanted to see I could find a way to pass it through the callback.
        self.__receiveUserDataType = ctypes.py_object(self.__receiveUserData)

        return (self.__UUIRTSetReceiveCallback(self.__dev_handle, self.__receiveCallback,
                                               ctypes.cast(ctypes.addressof(self.__receiveUserDataType),
                                                           ctypes.c_void_p)))

    def getUUIRTGPIOCfg(self):
        """Wraps UUIRTGetUUIRTGPIOCFG. Returns a tuple of int(), int(), usbuirt.UUGPIO()."""
        if not self.__opened:
            raise Exception
        gpiostruct = UUGPIO()
        pnumslots = ctypes.c_int(0)
        pdwportpins = ctypes.c_uint32(0)
        rv = self.__UUIRTGetUUIRTGPIOCfg(self.__dev_handle, ctypes.byref(pnumslots), ctypes.byref(pdwportpins),
                                         ctypes.byref(gpiostruct))
        if rv == 0:
            raise Exception
        return (int(pnumslots.value), int(pdwportpins.value), gpiostruct)

    def setUUIRTGPIOCfg(self, index, uugpio):
        """Wraps UUIRTSetUUIRTGPIOCfg.  Accepts an int() and a usbuirt.UUGPIO()."""
        if not self.__opened:
            raise Exception
        return (self.__UUIRTSetUUIRTGPIOCfg(self.__dev_handle, ctypes.c_int(index), ctypes.byref(uugpio)) == 1)

    def convertReverseBitCharacter(self, code):
        # Convert to integer
        code = int(code, 16)  # Hex Str -> Int
        inverseCode = (~code & 0xFF)  # Get Inverse Value

        # Convert to bit character
        code = "{0:08b}".format(code)
        inverseCode = "{0:08b}".format(inverseCode)

        # Reverse bit character
        code = code[::-1]
        inverseCode = inverseCode[::-1]

        return code + inverseCode

    def generateIrCode(self, keyCode, customCode='04'):
        irCode = "F41R0999815980AC"
        keyCode = self.convertReverseBitCharacter(keyCode)
        print(keyCode)
        customCode = self.convertReverseBitCharacter(customCode)
        temp = customCode + keyCode
        for bit in temp:
            if bit == '1':
                irCode += BIT_1
            else:
                irCode += BIT_0
        irCode += '16'
        return irCode

    def generateIrCode_for_panasonic(self, keyCode, customCode='04'):
        irCode = "F41R0999815980AC"
        keyCode = self.convertReverseBitCharacter(keyCode)
        print(keyCode)
        customCode = self.convertReverseBitCharacter(customCode)
        temp = customCode + keyCode
        for bit in temp:
            if bit == '1':
                irCode += BIT_1
            else:
                irCode += BIT_0
        irCode += '16'
        return irCode

    def generateIrCode_for_e_blackboard(self, keyCode, customCode='20'):
        irCode = "F42R0305815680AB"
        keyCode = self.convertReverseBitCharacter(keyCode)
        print(keyCode)
        customCode = self.convertReverseBitCharacter(customCode)
        temp = customCode + keyCode
        for bit in temp:
            if bit == '1':
                irCode += BIT_1
            else:
                irCode += BIT_0
        irCode += '16'
        return irCode

    def sendIrCode(self, code, repeat, type=LG_REMOTE):
        self.open("")
        if type == self.LG_REMOTE:
            irCode = self.generateIrCode(keyCode=code)
        elif type == self.E_BLACK_BOARD_REMOTE:
            irCode = self.generateIrCode_for_e_blackboard(keyCode=code)
        result = self.transmitIR(irCode, IRFMT_UUIRT, repeat, 100000)
        self.close()
        return result, irCode

    def sendDirectIrCode(self, irCode, repeat):
        self.open("")
        result = self.transmitIR(irCode, IRFMT_UUIRT, repeat, 100000)
        self.close()
        return result, irCode


def callbackFunc(r1, r2, r3, r4):
    print('R1: ' + str(r1))
    print('R2: ' + str(r2))
    print('R3: ' + str(r3))
    print('R4: ' + str(r4))
    print('=' * 30)


if __name__ == '__main__':
    irt = UsbUirt()
    irt.open()
    irt.sendIrCode(IrCodes.KEY_POWER, 1, irt.LG_REMOTE)
    
    #
    #     F41R0312815480A9 : 8bit
    #     15151515154115151516151615151516154115411516154115411541154115411541154115161541154115411541154115161516154115151516151515161516
    #     1515 1515 1541 1515 1516 1516 1515 1516 0 0 1 0 0 0 0 0 Address
    #     1541 1541 1516 1541 1541 1541 1541 1541 1 1 0 1 1 1 1 1 !Address
    #     1541 1541 1516 1541 1541 1541 1541 1541 1 1 0 1 1 1 1 1 Command
    #     1516 1516 1541 1515 1516 1515 1516 1516 0 0 1 0 0 0 0 0 !Command
    #     15|074E81545615
    #     15: Std Value * 1000 * 30(1,0의 시간차)
    #
    # print('-----')
    # irt.changSignalBitToHexString('F42R0316815780AC1615161516401615161516151615161516401640161516401640164016401640164016151615161516401615161516151615164016401640161516401640164016|076581575616')

    print('Listening...')
    print(irt.learnIR(IRFMT_UUIRT, callbackFunc, None, False, 0))

    # 32bit python에서만 돌아감!!!!

    # 0010 0000 1101 1111 1000 1000 0111 0111
    # |-Adress-|-Reverse-|--Data--|-Reverse-|