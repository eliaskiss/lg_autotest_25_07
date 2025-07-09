from pynput import keyboard
from pynput.keyboard import Key

def on_press(key):
    print(f'Key {key} press')

def on_release(key):
    print(f'Key {key} release')
    with open('key.log', 'a', encoding='utf8') as f:
        try:
            f.write(f'Key {key.char} pressed\n')
        except:
            pass
    if key == Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print('Keyboard is listening...')
    listener.join()

# # 생성후 메뉴얼로 시작
# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()
# listener.join()

print("Keyboard's listener is dead!")
