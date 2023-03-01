import schedule
import time


class TimersKeeper:
    jobs = {}

    def __init__(self, update_time):
        self.update_time = update_time

    def add(self, user_id, send_time, job_to_do):
        if len(send_time) < 5:
            job_time = "0{}".format(send_time)
        else:
            job_time = send_time
        self.jobs[user_id] = schedule.every().day.at(job_time).do(job_to_do)
        print("Schedule job for {} at {}".format(user_id, job_time))

    def delete(self, user_id):
        self.jobs.pop(user_id)
        print("Remove job for {}".format(user_id))

    def run_timer(self):
        while True:
            schedule.run_pending()
            time.sleep(self.update_time)
