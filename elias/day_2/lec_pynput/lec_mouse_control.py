from pynput.mouse import Button, Controller
import time

class RemoteMouse:
    def __init__(self):
        self.mouse = Controller()

    # Read current position
    def getPosition(self):
        return self.mouse.position

    # Set Pointer absolute position
    def setPos(self, xPos, yPos):
        self.mouse.position = (xPos, yPos)

    # Move Pointer relative to current position
    def movePos(self, xPos, yPos):
        self.mouse.move(xPos, yPos)

    # Click Left Button
    def click(self):
        # self.mouse.press(Button.left)
        # self.mouse.release(Button.left)
        self.mouse.click(Button.left)

    # Click Left Button
    def clickRight(self):
        # self.mouse.press(Button.right)
        # self.mouse.release(Button.right)
        self.mouse.click(Button.right)

    # Click Left Button
    def doubleClick(self):
        self.mouse.click(Button.left, 2)

    # Drag mouse
    def drag(self, from_x, from_y, to_x, to_y):
        self.mouse.position = (from_x, from_y)
        self.mouse.press(Button.left)
        self.mouse.position = (to_x, to_y)
        # Sleep이 있어야만 드래그가 가능
        time.sleep(0.1)
        self.mouse.release(Button.left)

    # Scroll
    # dx: (+) right, (-) left
    # dy: (+) up, (-) down
    def scroll(self, dx, dy):
        self.mouse.scroll(dx, dy)

    def scrollLeft(self, value):
        self.mouse.scroll(value * -1, 0)

    def scrollRight(self, value):
        self.mouse.scroll(value, 0)

    def scrollUp(self, value):
        self.mouse.scroll(0, value);

    def scrollDown(self, value):
        self.mouse.scroll(0, value * -1)

if __name__ == "__main__":
    mouse = RemoteMouse()

    # Get current position
    # print('Current mouse position:', mouse.getPosition())

    # Set Mouse position
    # mouse.setPos(0, 0)

    # Move Mouse position
    # mouse.movePos(100, 100)

    # Double Click
    # mouse.setPos(1277, 17)
    # mouse.doubleClick()

    # Drag Mouse
    # mouse.drag(417, 235, 1148, 235)

    # Scroll, righ & up
    # mouse.scroll(100, 1000)
    # mouse.scrollUp(1000)
