import time

class StringBuffer:
    buffers = {}

    def __init__(self, stream_id, buffer_size):
        """
        Init in the dict map the new stream_id if not exists
        """
        if stream_id not in StringBuffer.buffers:
            StringBuffer.buffers[stream_id] = {
                'buffer_size': buffer_size,
                'buffer': ""
            }
        self.buffer = StringBuffer.buffers[stream_id]['buffer']
        self.buffer_size = StringBuffer.buffers[stream_id]['buffer_size']

    def add(self, text):
        """
        Adds text to the buffer. If the buffer exceeds the buffer_size, it flushes.
        :param text: The text to add to the buffer.
        """
        self.buffer += text
        while len(self.buffer) >= self.buffer_size:
            self.flush()

    def flush(self):
        """
        Prints the contents of the buffer up to the buffer size and resets it.
        """
        buffer_piece = self.buffer[:self.buffer_size]
        print(f'{buffer_piece}    -({len(buffer_piece)})')
        self.buffer = self.buffer[self.buffer_size:]


# Example Usage
start_time = time.time()

# buffer1 = StringBuffer(stream_id=123, buffer_size=5)
# buffer2 = StringBuffer(stream_id=456, buffer_size=10)
# buffer1.add("Hello")
# buffer2.add("im using only small letters which is a bit weird")
# buffer1.add(", World!")
# buffer2.add("every time i flush i will print 10 characters")
# buffer2.add("do re me")
# buffer1.add("Again and again")

for i in range(1000):
    buffer1 = StringBuffer(stream_id=123, buffer_size=5)
    buffer2 = StringBuffer(stream_id=456, buffer_size=10)
    buffer1.add("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    buffer2.add("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    # Execution Time: 0.015397787094116211 seconds


end_time = time.time()
print(f"Execution Time: {end_time - start_time} seconds") # Execution Time: 4.029273986816406e-05 seconds