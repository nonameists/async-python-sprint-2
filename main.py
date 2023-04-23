from job import Job
from scheduler import Scheduler
from tasks import hello_world, hello_world2, hello_world3


def main():
    scheduler = Scheduler()
    job_2 = Job(name="second_job", func=hello_world2)
    job_3 = Job(name="thirdjob", func=hello_world3)
    dep_jobs = [job_2, job_3]
    job_1 = Job(name="first_job", func=hello_world, dependencies=dep_jobs)
    scheduler.schedule(job_1)
    scheduler.run()

if __name__ == '__main__':
    main()