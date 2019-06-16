from Timetable import Timetable
import time



timetable = Timetable('timetable.json')


while True:
    time.sleep(1)
    timetable.print_curr_task()
