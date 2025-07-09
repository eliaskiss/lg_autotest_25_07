from pynput.keyboard import Key, Controller
import time # sleep()

class RemoteKeyboard:
    def __init__(self):
        self.keyboard = Controller()

    # Press key and release
    def inputKey(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    # Press key with ALT
    def inputKeyWithAlt(self, key):
        with self.keyboard.pressed(Key.alt):
            self.keyboard.press(key)
            self.keyboard.release(key)

    # Press key with Shift
    def inputKeyWithShift(self, key):
        with self.keyboard.pressed(Key.shift):
            self.keyboard.press(key)
            self.keyboard.release(key)

    # Press key with Ctrl
    def inputKeyWithCtrl(self, key):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press(key)
            self.keyboard.release(key)

    # Press key with special key
    def inputKeyWith(self, with_key, key):
        with self.keyboard.pressed(with_key):
            self.keyboard.press(key)
            self.keyboard.release(key)

    # Enter Key
    def enter(self):
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    # Type string
    def typeString(self, string):
        self.keyboard.type(string)

if __name__ == "__main__":
    kb = RemoteKeyboard()
    time.sleep(10)

    kb.inputKey('a')
    time.sleep(1)
    kb.inputKey(Key.enter)
    time.sleep(1)
    kb.inputKey('A')
    time.sleep(1)
    kb.inputKeyWithCtrl('v')
    time.sleep(1)
    kb.typeString('Hi')
    time.sleep(1)

