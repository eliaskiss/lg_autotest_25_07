from pynput import mouse
from pynput.mouse import Button
from pynput import keyboard

def on_click(x, y, button, pressed):
    with open('../kb_mouse.log', 'a') as f:
        f.write('[%d:%d]\n' % (x, y))

    if button == Button.right and not pressed:
        print('Mouse listener is dead!!')
        return False

def on_release(key):
    with open('../kb_mouse.log', 'a') as f:
        try:
            f.write('[%s]\n' % key.char)
        except:
            f.write('[%s]\n' % key)

    if key == keyboard.Key.esc:
        print('Keyboard listener is dead!!')
        return False

with mouse.Listener(on_click=on_click) as mouse_listener:
    with keyboard.Listener(on_release=on_release) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()


# mouse_listener = mouse.Listener(on_click=on_click)
# mouse_listener.start()
# mouse_listener.join()
#
# keyboard_listener = keyboard.Listener(on_release=on_release)
# keyboard_listener.start()
# keyboard_listener.join()