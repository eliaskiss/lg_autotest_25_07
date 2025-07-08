import asyncio
import serial_asyncio

class OutputProtocol(asyncio.Protocol):
    read_buffer = b''

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        # readed = repr(data)
        # print(type(readed))
        # print(type(self.read_buffer))
        # print('data received', readed)
        self.read_buffer += data
        if b'\r' in data:
            print(self.read_buffer)
            self.read_buffer = b''

        if b'\n' in data:
            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = serial_asyncio.create_serial_connection(loop, OutputProtocol, 'com2', baudrate=9600)
    transport, protocol = loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()