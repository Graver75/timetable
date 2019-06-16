import json, os
from datetime import datetime, timedelta


class Timetable:
    def __init__(self, filename):
        self.filename = filename
        self.now = datetime.now()
        self._temp_now = None

        self._read_data()
        self._normalize_data()
        self._parse_data()

    def __str__(self):
        result = ""
        for day in self.timetable:
            result += (day[0].strftime("%A") + " " + day[0].strftime("%Y-%m-%d") + "\n")
            for task in day[1]:
                result += ("\t " + task[0] + " " + ("{:d}:{:02d}".format(task[1].hour, task[1].minute)) + " \n")

        return result

    def _read_data(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)

            self._start_time = data["start_time"]
            self._diff = data["diff_time"]
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

    def _parse_day(self, tasks):
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
        self.timetable = []

        for i in range(7):
            curr_day = self._get_day_after_day(self.now, i)
            self.timetable.append((curr_day, self._parse_day(self._days[curr_day.strftime("%A")])))

    def _get_curr_day_task(self):
        now = datetime.now()
        result = None
        for day_task in self.timetable:
            date = day_task[0]
            if now.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
                result = day_task
        return result

    def _get_around_tasks(self):
        current_tasks = self._get_curr_day_task()[1]
        now = datetime.now()

        curr_task = None
        next_task = None

        for i in range(len(current_tasks) - 1):
            prev = current_tasks[i][1]
            curr = current_tasks[i + 1][1]
            if prev < now < curr:
                curr_task = current_tasks[i]
                next_task = current_tasks[i + 1]
        return (curr_task, next_task)

    def print_curr_task(self):
        curr_task, next_task = self._get_around_tasks()

        os.system('clear')
        now = datetime.now()

        print("Current time: ", now)
        print("Current task: ", curr_task[0])
        print("Remaining time: ", next_task[1] - now)
        print("Next task is " + next_task[0] + " at ", next_task[1].strftime("%H:%M:%S"))