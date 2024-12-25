from collections import OrderedDict
import time
from typing import Any

class LRUCache:

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.called_times = {}
        self.end_of_ttl = {}

    def get(self, key: int) -> Any:
        if self.end_of_ttl.get(key) and self.end_of_ttl[key] < time.time():
            self.end_of_ttl.pop(key)
            self.cache.pop(key)
        if self.called_times.get(key, 0) == 5:
            self.called_times.pop(key)
            self.cache.pop(key)
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            self.called_times[key] += 1
            return self.cache[key]

    def put(self, key: int, value: Any, ttl: float = -1) -> None:
        self.cache[key] = value
        self.called_times[key] = 0
        if ttl > 0:
            self.end_of_ttl[key] = time.time() + ttl
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)

import threading

class EagerLRUCache(LRUCache):
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.cleanup_thread = threading.Thread(target=self._cleanup, daemon=True)
        self.cleanup_thread.start()

    def _cleanup(self):
        while True:
            current_time = time.time()
            expired_keys = [key for key, expiry in self.end_of_ttl.items() if expiry < current_time]
            for key in expired_keys:
                self.end_of_ttl.pop(key)
                self.cache.pop(key, None)
            time.sleep(0.1)  # Periodic check every 0.1 seconds




cache = EagerLRUCache(2)

cache.put(1, 'one')
print("the value one should exist in the cache")
print(cache.get(1))
print("the value one should exist in the cache")
print(cache.get(1))
print("the value one should exist in the cache")
print(cache.get(1))
print("the value one should exist in the cache")
print(cache.get(1))
print("the value one should exist in the cache")
print(cache.get(1))
print("the value one shouldn't exist in the cache")
print(cache.get(1))


print()
print('*******')
print()


cache.put(2, 'two', 0.5)
print("the value two should exist in the cache")
print(cache.get(2))
time.sleep(1)
print("the value two shouldn't exist in the cache")
print(cache.get(2))



