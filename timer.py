import threading
import time
import random as r


class TimeMeter:
    def __init__(self):
        self._lock = threading.Lock()
        self._global_time = 0

    def get_global_time(self):
        with self._lock:
            return self._global_time

    def increment_global_time(self, increment):
        with self._lock:
            self._global_time += increment


def time_updater(time_meter):
    while True:
        time.sleep(0.1)  # Espera 1 segundo
        time_meter.increment_global_time(1)  # Incrementa el tiempo global en 1 segundo


class MiClase:
    def __init__(self, name, time_meter):
        self.name = name
        self.time_meter = time_meter

    def do_something(self):
        while True:
            current_time = self.time_meter.get_global_time()
            print(f"{self.name} - Global Time: {current_time}")
            i = r.randint(1, 5)
            time.sleep(i)


