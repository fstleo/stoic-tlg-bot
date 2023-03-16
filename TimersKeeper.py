import schedule
import time


class TimersKeeper:
    jobs = dict()

    def __init__(self, update_time):
        self.update_time = update_time

    def add(self, user_id, send_time, job_to_do):
        job_time = send_time.strftime("%H:%M")
        self.jobs[user_id] = schedule.every().day.at(job_time).do(job_to_do)
        print("Schedule job for {} at {}".format(user_id, job_time))

    def delete(self, user_id):
        job = self.jobs.pop("{}".format(user_id))
        schedule.cancel_job(job)
        print("Remove job for {}".format(user_id))

    def run_timer(self):
        while True:
            schedule.run_pending()
            time.sleep(self.update_time)
