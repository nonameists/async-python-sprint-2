from job import Job
from scheduler import Scheduler
from tasks import create_directory, create_file, get_request, hello_world, hello_world_2, hello_world_3


def main():
    scheduler = Scheduler()
    job_1 = Job(name="create_dir_job", func=create_directory)
    job_2 = Job(name="create_file_job", func=create_file)
    job_3 = Job(name="url_request_job", func=get_request, max_working_time=5)

    hello_job_dependencies = [
        Job(name="hello_world_2_task", func=hello_world_2),
        Job(name="hello_world_3_task", func=hello_world_3)
    ]
    job_4 = Job(name="hello_world_task", func=hello_world, dependencies=hello_job_dependencies)

    scheduler.schedule(job_1)
    scheduler.schedule(job_2)
    scheduler.schedule(job_3)
    scheduler.schedule(job_4)

    scheduler.run()


if __name__ == '__main__':
    main()
