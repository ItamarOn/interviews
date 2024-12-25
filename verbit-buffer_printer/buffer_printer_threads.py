import threading
import time

class StringBufferThread:
    buffers = {}
    lock = threading.Lock()

    def __init__(self, stream_id, buffer_size):
        """
        Initializes a StringBufferThread instance, creating a unique buffer for each stream_id.
        Uses threads internally to handle flush operations concurrently.
        """
        with StringBufferThread.lock:
            if stream_id not in StringBufferThread.buffers:
                # Each stream gets its own buffer and lock
                StringBufferThread.buffers[stream_id] = {
                    'buffer_size': buffer_size,
                    'buffer': "",
                    'lock': threading.Lock(),
                    'thread': None
                }
        self.stream_id = stream_id

    def add(self, text):
        """
        Adds text to the buffer. Flushes whenever the buffer exceeds the buffer size.
        """
        with StringBufferThread.buffers[self.stream_id]['lock']:
            buffer_data = StringBufferThread.buffers[self.stream_id]
            buffer_data['buffer'] += text

            if not buffer_data['thread'] or not buffer_data['thread'].is_alive():
                # Start a flush thread if not already running
                buffer_data['thread'] = threading.Thread(target=self._flush_thread, daemon=True)
                buffer_data['thread'].start()

    def _flush_thread(self):
        """
        A thread function to flush the buffer only when it reaches the required size.
        """
        buffer_data = StringBufferThread.buffers[self.stream_id]
        while True:
            with buffer_data['lock']:
                # Flush only full buffer pieces
                if len(buffer_data['buffer']) < buffer_data['buffer_size']:
                    break  # Exit if there isn't enough content to flush
                buffer_piece = buffer_data['buffer'][:buffer_data['buffer_size']]
                print(f"[Stream {self.stream_id}] {buffer_piece}    -({len(buffer_piece)})")
                buffer_data['buffer'] = buffer_data['buffer'][buffer_data['buffer_size']:]

# Example Usage
start_time = time.time()

# buffer1 = StringBufferThread(stream_id=123, buffer_size=5)
# buffer2 = StringBufferThread(stream_id=456, buffer_size=10)
# buffer1.add("Hello")
# buffer2.add("im using only small letters which is a bit weird")
# buffer1.add(", World!")
# buffer2.add("every time i flush i will print 10 characters")
# buffer2.add("do re me")
# buffer1.add("Again and again")

for i in range(1000):
    buffer1 = StringBufferThread(stream_id=123, buffer_size=5)
    buffer2 = StringBufferThread(stream_id=456, buffer_size=10)
    buffer1.add("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    buffer2.add("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    # Execution Time: 0.11259627342224121 seconds
    
end_time = time.time()
print(f"Execution Time: {end_time - start_time} seconds")  # Execution Time: 0.0004711151123046875 seconds
