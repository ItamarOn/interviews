
class MultiTimer:
    def __init__(self):
        """
        timmers = {
            30: (now(), callback1)
        """
        self.timers = {}
        self.passed_time = now()

    def schedule(self, seconds, callback):
        self.update_timers()
        self.add_task(seconds, callback)

        self.run_all_tasks()

    def self.update_timers():
        current_time = now()
        passed_time = current_time - self.passed_time
        self.passed_time = current_time

        for key in self.timers.keys():
            self.timers[key] -= passed_time

    def run_all_tasks(self):
        next_key, next_val = self.timers.pop()
        tmp = now()

        # 30
        SingleTimer.schedule(next_key, next_val)



    def add_task(self, seconds, callback):
        if self.is_running:


        min = min(self.timers.keys())

        if seconds < min:
            SingleTimer.cancel()

        self.timers[seconds] = callback

        SingleTimer.schedule(seconds, callback)
