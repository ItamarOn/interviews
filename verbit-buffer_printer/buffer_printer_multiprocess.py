import multiprocess as multiprocessing
import time

class StringBufferProcess:
    manager = multiprocessing.Manager()
    buffers = manager.dict()
    locks = manager.dict()

    def __init__(self, stream_id, buffer_size):
        """
        Initializes a StringBufferProcess instance, creating a unique buffer for each stream_id.
        Uses multiprocessing internally to handle flush operations concurrently.
        """
        if stream_id not in StringBufferProcess.buffers:
            # Each stream gets its own buffer and lock
            StringBufferProcess.buffers[stream_id] = {
                'buffer_size': buffer_size,
                'buffer': ""
            }
            StringBufferProcess.locks[stream_id] = multiprocessing.Lock()
        self.stream_id = stream_id

    def add(self, text):
        """
        Adds text to the buffer. Flushes whenever the buffer exceeds the buffer size.
        """
        with StringBufferProcess.locks[self.stream_id]:
            buffer_data = StringBufferProcess.buffers[self.stream_id]
            buffer_data['buffer'] += text

            if len(buffer_data['buffer']) >= buffer_data['buffer_size']:
                process = multiprocessing.Process(target=self._flush_process)
                process.start()
                process.join()

    def _flush_process(self):
        """
        A process function to flush the buffer only when it reaches the required size.
        """
        with StringBufferProcess.locks[self.stream_id]:
            buffer_data = StringBufferProcess.buffers[self.stream_id]
            while len(buffer_data['buffer']) >= buffer_data['buffer_size']:
                buffer_piece = buffer_data['buffer'][:buffer_data['buffer_size']]
                print(f"[Stream {self.stream_id}] {buffer_piece}    -({len(buffer_piece)})")
                buffer_data['buffer'] = buffer_data['buffer'][buffer_data['buffer_size']:]


# Example Usage
if __name__ == "__main__":
    start_time = time.time()

    buffer1 = StringBufferProcess(stream_id=123, buffer_size=5)
    buffer2 = StringBufferProcess(stream_id=456, buffer_size=10)
    buffer1.add("Hello")
    buffer2.add("im using only small letters which is a bit weird")
    buffer1.add(", World!")
    buffer2.add("every time i flush i will print 10 characters")
    buffer2.add("do re me")
    buffer1.add("Again and again")

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")


#     raise RuntimeError(
# RuntimeError: Lock objects should only be shared between processes through inheritance