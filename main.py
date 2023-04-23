from job import Job
from scheduler import Scheduler
from tasks import hello_world


def main():
    scheduler = Scheduler()
    job_1 = Job(name="first_job", func=hello_world)
    scheduler.schedule(job_1)
    scheduler.run()

if __name__ == '__main__':
    main()