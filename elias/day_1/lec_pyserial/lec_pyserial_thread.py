import threading
from lec_pyserial_class import Serial
import time

read_is_running = False
write_is_running = False

def thread_read_func(serial, interval=None):
    global read_is_running

    print('ReadThread is started')
    read_is_running = True
    print('Timeout:', interval)
    while read_is_running:
        readed = serial.readLine(interval)
        print('Readed:', readed)
    print('ReadThread is dead')

def thread_write_func(serial, interval):
    global write_is_running

    print('WriteThread is started')
    write_is_running = True
    print('Interval:', interval)
    count = 0
    while write_is_running:
        count += 1
        data = f'HelloWorld_{count}\r\n'
        written = serial.writePortUnicode(data)
        print('Written:', data, written)
        time.sleep(interval)
    print('WriteThread is dead')

if __name__ == '__main__':
    serial = Serial()
    serial.openPort('com2')

    rt = threading.Thread(target=thread_read_func, args=[serial, 1])
    rt.start()
    # print('isAlive:', rt.is_alive())
    # print(t.isDaemon())
    # t.setDaemon(True)

    wt = threading.Thread(target=thread_write_func, args=[serial, 3])
    wt.start()

    time.sleep(30)
    read_is_running = False
    write_is_running = False
    # print('isAlive:', t.is_alive())
