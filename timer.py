import time as t


class Time:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def set_time(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def add_seconds(self, seconds):
        total_seconds = self.hour * 3600 + self.minute * 60 + self.second + seconds
        self.hour = total_seconds // 3600
        self.minute = (total_seconds % 3600) // 60
        self.second = (total_seconds % 3600) % 60

        print(self.hour, self.minute, self.second)
