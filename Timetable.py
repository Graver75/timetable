import json
from datetime import datetime, timedelta

class Timetable:
    def __init__(self, filename):
        self.filename = filename
        self.now = datetime.now()
        self._temp_now = None

        self._read_data()
        self._normalize_data()
        self._parse_data()

    def _read_data(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)

            self._start_time = data["start_time"]
            self._diff = data["diff_time"]
            self._finish_time = data["finish_time"]
            self._days = data["days"]

    def _get_day_after_day(self, d, n):
        return d + timedelta(days=n)

    def _get_hour_after_hour(self, d, n):
        return d + timedelta(hours=n)

    def _parse_tasks(self, tasks):
        amount_hours = 0
        l = []
        for task in tasks:
            task, amount = task.split('_')
            amount_hours += int(amount)
            for i in range(int(amount)):
                l.append(task)
        return l, amount_hours

    def _normalize_data(self):
        pre_days = {}
        for day in self._days:
            if isinstance(self._days[day], list):
                pre_days[day] = self._days[day]
            else:
                pre_days[day] = pre_days[self._days[day]]
        self._days = pre_days

    def _parse_day(self, d, tasks):
        day_tasks = []
        tasks, amount = self._parse_tasks(tasks)

        if not self._temp_now:
            start_time = self.now.replace(hour=int(self._start_time[:2]), second=0, microsecond=0, minute=int(self._start_time[3:]))
        else:
            start_time = self._temp_now.replace(hour=int(self._start_time[:2]), second=0, microsecond=0, minute=int(self._start_time[3:]))
        temp_time = None

        for i in range(amount):
            curr_time = self._get_hour_after_hour(start_time, i)
            day_tasks.append((tasks[i], curr_time))
            temp_time = curr_time
        self._temp_now = temp_time
        return day_tasks


    def _parse_data(self):
        self._timetable = []

        for i in range(7):
            curr_day = self._get_day_after_day(self.now, i)
            self._timetable.append((curr_day, self._parse_day(curr_day, self._days[curr_day.strftime("%A")])))
