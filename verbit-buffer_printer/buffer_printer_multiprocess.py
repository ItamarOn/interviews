import time
from multiprocessing import Process


def printer(buffer_piece):
    print(f'{buffer_piece}    -({len(buffer_piece)})')


class StringBufferProcess:
    buffers = {}
    processes = []

    def __init__(self, stream_id, buffer_size):
        """
        Init in the dict map the new stream_id if not exists
        """
        if stream_id not in StringBufferProcess.buffers:
            StringBufferProcess.buffers[stream_id] = {
                'buffer_size': buffer_size,
                'buffer': ""
            }
        self.buffer = StringBufferProcess.buffers[stream_id]['buffer']
        self.buffer_size = StringBufferProcess.buffers[stream_id]['buffer_size']

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
        process = Process(target=printer, args=(buffer_piece,))
        self.processes.append(process)
        process.start()
        self.buffer = self.buffer[self.buffer_size:]

    @classmethod
    def collect_processes(cls):
        for process in cls.processes:
            process.join()



# Example Usage
if __name__ == "__main__":
    start_time = time.time()
    #
    buffer1 = StringBufferProcess(stream_id=123, buffer_size=5)
    buffer2 = StringBufferProcess(stream_id=456, buffer_size=10)
    buffer1.add("Hello")
    buffer2.add("im using only small letters which is a bit weird")
    buffer1.add(", World!")
    buffer2.add("every time i flush i will print 10 characters")
    buffer2.add("do re me")
    buffer1.add("Again and again")


    # buffer1 = StringBufferProcess(stream_id=123, buffer_size=5)
    # buffer2 = StringBufferProcess(stream_id=456, buffer_size=10)
    #
    # for i in range(10000):
    #     buffer1.add("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     buffer2.add("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    #     # OSError: [Errno 24] Too many open files

    StringBufferProcess.collect_processes()
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")  # Execution Time: 4.029273986816406e-05 seconds
