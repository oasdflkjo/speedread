from collections import deque
import time


class AverageWPM:
    def __init__(self, buffer_size=50):
        self.buffer = deque(maxlen=buffer_size)
        self.last_call_time = time.time()
        self.first_call = True

    def get_average_wpm(self):
        current_time = time.time()
        time_diff = current_time - self.last_call_time

        if time_diff > 0:
            wpm = (60 / time_diff) if self.buffer else 0
            self.buffer.append((wpm, time_diff))

        self.last_call_time = current_time

        average_wpm = sum(wpm for wpm, _ in self.buffer) / \
            len(self.buffer) if self.buffer else 0

        # debug print for now
        print(average_wpm, flush=True)
        return average_wpm
