import asyncio
import serial_asyncio


class InputChunkProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print('data received', repr(data))

        # stop callbacks again immediately
        self.pause_reading()

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()


async def reader():
    transport, protocol = await serial_asyncio.create_serial_connection(loop, InputChunkProtocol, 'com2', baudrate=9600)

    while True:
        await asyncio.sleep(1)
        protocol.resume_reading()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(reader())
    loop.close()