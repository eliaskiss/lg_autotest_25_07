from pynput import mouse
from pynput.mouse import Button

def on_move(x, y):
    print('Pointer moved to {0}'.format((x,y)))
    pass

def on_click(x, y, button, pressed):
    print(f'Mouse Clicked position: ({x}, {y})')
    print(f'Button: {button}')
    print(f'Pressed: {pressed}')

    if pressed is False:
        with open('mouse.log', 'a', encoding='utf8') as f:
            f.write(f'Mouse Clicked position: ({x}, {y})\n')
            f.write(f'Button: {button}\n')

    if button == Button.right and not pressed:
        return False

def on_scroll(x, y, dx, dy):
    print(f"Scrolled {'down' if dy < 0 else 'up'} at {(x,y)}")
    print(f"Scrolled {'left' if dx < 0 else 'right'} at {(x, y)}")
    with open('mouse.log', 'a', encoding='utf8') as f:
        f.write(f"Scrolled {'down' if dy < 0 else 'up'} at {(x,y)}\n")
        f.write(f"Scrolled {'left' if dx < 0 else 'right'} at {(x, y)}\n")

with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    print('Mouse is listening...')
    listener.join()

# 생성후 메뉴얼로 시작
# listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
# listener.start()
# listener.join()

print("Mouse's listener is dead!")