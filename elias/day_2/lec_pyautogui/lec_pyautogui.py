import pyautogui
from icecream import ic
from pyautogui import *
import time
from datetime import datetime, timedelta

class AutoGui:
    # Screen Size (Only Main Screen)
    def getScreenSize(self):
        screen_size = pyautogui.size()
        return screen_size

    # Current Mouse position
    def getMousePosition(self):
        current_pos = pyautogui.position()
        return current_pos

    # Check Position Validation
    def isValidPosition(self, pos_x, pos_y):
        valid = pyautogui.onScreen(pos_x, pos_y)
        return valid

    # Set/Get pause time for each call of pyautogui
    def setPauseTime(self, sec):
        pyautogui.PAUSE = sec

    def getPauseTime(self):
        return pyautogui.PAUSE

    # Fail-Safe : Over FAILSAFE_POINTS and FAILSAFE is True, occurs "pyautogui.FailSafeException"
    def setFailSafeMode(self, enable):
        pyautogui.FAILSAFE = enable

    def getFailSafeMode(self):
        return pyautogui.FAILSAFE

    ############################################################################################################
    # 0, 0        X    increases -->
    # +---------------------------+
    # |                           | Y    increases
    # |                           |       |
    # | 1920    x    1080  screen |       |
    # |                           |       V
    # |                           |
    # |                           |
    # +---------------------------+ 1919, 1079

    # Move mouse pointer
    def mouseMove(self, pos_x, pos_y, duration=0, relative=False):
        if relative is True:
            pyautogui.moveRel(pos_x, pos_y, duration)
        else:
            pyautogui.moveTo(pos_x, pos_y, duration)

    # Drage Mouse (현재 위치에서 pos_x, pos_y까지 duration 동안 드래그)
    def mouseDrag(self, pos_x, pos_y, duration=0.2, relative=False):
        # duration을 0.2미만으로 설정하게되면 드래그가 안됨
        if duration < 0.2:
            duration = 0.2

        if relative is True:
            # pyautogui.dragRel(float(pos_x), float(pos_y), duration) # 현재위치 부터 x, y 만큼
            pyautogui.dragRel(pos_x, pos_y, duration)  # 현재위치 부터 x, y 만큼
        else:
            # pyautogui.dragTo(float(pos_x), float(pos_y), duration)  # 현재위치 부터 x, y 까지
            pyautogui.dragTo(pos_x, pos_y, duration)  # 현재위치 부터 x, y 까지

    # Click mouse (pox_x, pos_y 위치를 interval 간격으로 num_of_click 회 button 클릭)
    def mouseClick(self, pos_x=None, pos_y=None, num_of_click=1, interval=0, button='left', logScreenshot=False):
        pyautogui.click(pos_x, pos_y, num_of_click, interval, button, logScreenshot=logScreenshot)

    def mouseRClick(self, pos_x=None, pos_y=None):
        pyautogui.rightClick(pos_x, pos_y)

    def mouseMClick(self, pos_x=None, pos_y=None):
        pyautogui.middleClick(pos_x, pos_y)

    def mouseDClick(self, pos_x=None, pos_y=None):
        pyautogui.doubleClick(pos_x, pos_y)

    # Vertical Scroll Mouse
    def mouseScrollUp(self, amount):
        pyautogui.scroll(amount)  # amount > 0 : Scroll Up, amount < 0: Scroll Down

    def mouseScrollDown(self, amount):
        pyautogui.scroll(amount * -1)

    # Horizontal Scroll Mouse(Only Mac & Linux, On Window Left->Down, Right->Up)
    def mouseScrollRight(self, amount):
        pyautogui.hscroll(amount)  # amount > 0 : Scroll Right, amount < 0: Scroll Left

    def mouseScrollLeft(self, amount):
        pyautogui.hscroll(amount * -1)

    ############################################################################################################
    # KEY_NAMES (only keyDown, keyUp, pressKey, hotKey)
    # ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    #  ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    #  '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    #  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    #  'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    #  'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
    #  'browserback', 'browserfavorites', 'browserforward', 'browserhome',
    #  'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
    #  'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
    #  'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
    #  'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    #  'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    #  'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
    #  'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
    #  'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
    #  'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    #  'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    #  'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
    #  'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
    #  'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
    #  'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
    #  'command', 'option', 'optionleft', 'optionright']

    # Type Keyboard (interval 간격으로 한글자씩 text 타이핑)
    def kbWrite(self, text, interval=0, logScreenshot=False):
        pyautogui.write(text, interval, logScreenshot=logScreenshot)

    # Press Keyboard key in KEY_NAMES
    def kbPressKey(self, key_name, presses=1, interval=0):
        pyautogui.press(key_name, presses, interval)

    # Press key combination
    def kbHotKey(self, *args, **kwargs):
        pyautogui.hotkey(*args, **kwargs)

    # Keep press key-down until call key-up
    def kbKeyDown(self, key_name):
        pyautogui.keyDown(key_name)

    # Release key-down
    def kbKeyUp(self, key_name):
        pyautogui.keyUp(key_name)

    ############################################################################################################
    # ScreenShot (Save to file or return as Image object of pillow
    def screenshot(self, file_name=None):
        img = pyautogui.screenshot(file_name)
        return img

    # Get Image location in screen (이미지 찾지못하면 예외발생)
    def getPositionOfImage(self, image_path, is_center=False, is_fast_mode=False):
        position = pyautogui.locateOnScreen(image_path, grayscale=is_fast_mode)
        print(position)
        if position is not None:
            if is_center:
                position = pyautogui.center(position)
            else:
                position = Point(position.left, position.top)
            return position
        else:
            return position

    def getPositionListOfImage(self, image_path, is_center=False, is_fast_mode=False):
        positions = list(pyautogui.locateAllOnScreen(image_path, grayscale=is_fast_mode))

        position_list = []
        for position in positions:
            if is_center:
                position_list.append(pyautogui.center(position))
            else:
                position_list.append(Point(position.left, position.top))
        return position_list

    # Click Image
    def clickImage(self, file_name):
        pyautogui.click(file_name)

if __name__ == '__main__':
    # AutoGui 객체생성
    ag = AutoGui()

    # # Get Screen Size
    # ic(ag.getScreenSize())

    # # Get Current Mouse Position
    # ic(ag.getMousePosition())

    # # Check Position Validation
    # ic(ag.isValidPosition(100, 100))
    # ic(ag.isValidPosition(2000, 2000))
    # ic(ag.isValidPosition(-1, -1))
    # ic(ag.isValidPosition(0, 0))
    # ic(ag.isValidPosition(1919, 1079))
    # ic(ag.isValidPosition(1920, 1080))

    # # Set Pause Time for each call function
    # default = ag.getPauseTime()
    # ic('Default Pause Time:', default)
    # ag.setPauseTime(1)
    # ic('New Pause Time:', ag.getPauseTime())
    # ag.setPauseTime(default)

    # Set Fail-Safe Mode : 범위벗어났을때 예외발생여부
    # ic('Default Fail-Safe Mode:', ag.getFailSafeMode())
    # ag.mouseMove(2000, 2000)
    # ag.setFailSafeMode(False)
    # ic('New Fail-Safe Mode:', ag.getFailSafeMode())
    # ag.mouseMove(2000, 2000)

    # Mouse Move
    # ag.mouseMove(1, 1) # (1, 1)위치로 이동
    # ag.mouseMove(500, 500, 3) # (500, 500)으로 3초 동안 이동
    # ag.mouseMove(100, 100) # (100, 100)으로 이동
    # ag.mouseMove(100, 100, 3, relative=True) # 현재 마우스 커서 위치 기준으로 (100, 100) 3초 동안 이동
    # ag.mouseMove(-100, -100, 3, relative=True) # 현재 마우스 커서 위치 기준으로 반대방향(100, 100) 3초 동안 이동

    # # Mouse Drag
    # ic(ag.getMousePosition())
    # ag.mouseMove(488, 104)  # (380, 310)으로 이동
    # ag.mouseDrag(500, 500, 3)   # (380, 310) -> (500, 500) 까지 3초동안 드래그
    # ag.mouseDrag(500, 500, 3, True) # (380, 310) -> (880, 810) 까지 3초 동안 드래그 [(500, 500) 만큼 드래그]

    # # Mouse Click
    # position = ag.getMousePosition()
    # ag.mouseClick(position.x, position.y, logScreenshot=True)

    # # Click button 3 times at 1 sec interval and screenshot
    # position = ag.getMousePosition()
    # ag.mouseClick(position.x, position.y, 3, 1, 'left', True)

    # # Double Click
    # position = ag.getMousePosition()
    # ag.mouseDClick(position.x, position.y)

    # # Right Click
    # position = ag.getMousePosition()
    # ag.mouseRClick(position.x, position.y)

    # Scroll Mouse
    # ag.mouseScrollUp(1000)
    # time.sleep(3)
    # ag.mouseScrollDown(1000)
    # ag.mouseScrollLeft(1000)      # Windows에서는 ScrollDown으로 동작
    # time.sleep(3)
    # ag.mouseScrollRight(1000)     # Windows에서는 ScrollUp으로 동작

    # KB Write
    # ag.kbWrite('Hello')
    # ag.kbWrite('Hello', 1, True) # 스크린샷 저장 후 1초간격으로 Hello를 한글자씩 입력

    # KB PressKey
    # ag.kbPressKey('win')      # Window 키
    # ag.kbPressKey('num0', 5, 1) # 1초 간격으로 0번키를 5번 입력

    # KB Hotkey
    # ag.kbHotKey('ctrl', 'shift', 'esc') # 작업관리자 실행

    # KB KeyDown/KeyUp
    # ag.kbKeyDown('ctrl')
    # ag.kbKeyDown('shift')
    # ag.kbKeyDown('esc')
    # ag.kbKeyUp('esc')
    # ag.kbKeyUp('shift')
    # ag.kbKeyUp('ctrl')

    # ScreenShot
    # now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # # ic(now)
    # # obj = datetime.strptime('[2023-08-24_08-24-14] ', '[%Y-%m-%d_%H-%M-%S] ')
    # # ic(obj)
    # yesterday = datetime.now() + timedelta(days=-1)
    # # yesterday = datetime.now() - timedelta(days=1)
    # ic(yesterday)
    # yesterday = yesterday.strftime('%Y_%m_%d_%H_%M_%S')
    # ag.screenshot(f'{yesterday}.png')

    # Get Position of Image
    # center_position = ag.getPositionOfImage('7.png', is_center=True)
    # ic(center_position)
    # ag.mouseClick(center_position)

    # # Get Position List of Image
    # position_list = ag.getPositionListOfImage('7.png', is_center=True)
    # for position in position_list:
    #     ic('Center Position:', position)
    #     ag.mouseClick(position.x, position.y)

    # # Click Image
    # ag.clickImage('7.png')

    # # 한글로 "안녕 파이썬" 입력
    # ag.kbHotKey('hangul')
    # ag.kbWrite('dkssud vkdlTjs')

    # # 전체코드를 복사하고, 노트패드를 열어서 붙여넣기
    # ag.setPauseTime(1)
    # ag.kbHotKey('ctrl', 'a', 'ctrl', 'c')
    # ag.kbHotKey('esc')
    # ag.kbHotKey('win', 'r')
    # ag.kbWrite('notepad\n')
    # ag.kbHotKey('ctrl', 'v')