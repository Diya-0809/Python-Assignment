"""
Q9 - Threaded Job Scheduler Simulation
"""
import threading
import heapq

class Job:
    def __init__(self, arrival, job_id, priority, duration, resources, order):
        self.arrival = arrival
        self.job_id = job_id
        self.priority = priority
        self.duration = duration
        self.resources = resources
        self.order = order

        self.start = -1
        self.finish = -1
        self.worker = -1

class Scheduler:
    def __init__(self, workers, jobs):
        self.workers = workers
        self.jobs = jobs

        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

        self.waiting = []
        self.current_time = 0

        self.next_job = 0
        self.completed = 0

        self.worker_available = [True] * workers

    def add_arrived_jobs(self):
        while (
            self.next_job < len(self.jobs)
            and self.jobs[self.next_job].arrival <= self.current_time
        ):
            job = self.jobs[self.next_job]

            # Higher priority first.
            # Earlier arrival first.
            # Input order is used as final tie-breaker.
            heapq.heappush(
                self.waiting,
                (
                    -job.priority,
                    job.arrival,
                    job.order,
                    job
                )
            )

            self.next_job += 1
            
    def get_free_worker(self):
        for i in range(self.workers):
            if self.worker_available[i]:
                return i

        return -1
        
    def worker_run(self, worker_id):

        while True:

            with self.condition:

                while True:

                    # Add jobs that have arrived.
                    self.add_arrived_jobs()

                    # Everything completed.
                    if self.completed == len(self.jobs):
                        return

                    # Find a free job for this worker.
                    if self.waiting and self.worker_available[worker_id]:

                        _, _, _, job = heapq.heappop(self.waiting)

                        self.worker_available[worker_id] = False

                        # A job cannot start before its arrival.
                        self.current_time = max(
                            self.current_time,
                            job.arrival
                        )

                        job.start = self.current_time
                        job.worker = worker_id + 1
                        job.finish = (
                            job.start + job.duration
                        )

                        break

                    # No currently executable job.
                    # Advance simulated time to the next arrival
                    # if no waiting jobs exist.
                    if not self.waiting and self.next_job < len(self.jobs):

                        next_arrival = self.jobs[
                            self.next_job
                        ].arrival

                        if next_arrival > self.current_time:
                            self.current_time = next_arrival

                            self.add_arrived_jobs()
                            continue

                    self.condition.wait()

            with self.condition:

                self.current_time = max(
                    self.current_time,
                    job.finish
                )

                self.worker_available[worker_id] = True
                self.completed += 1

                self.condition.notify_all()

# Main
w, n = map(int, input().split())

jobs = []

for order in range(n):

    arrival, job_id, priority, duration, resources = input().split()

    job = Job(
        int(arrival),
        job_id,
        int(priority),
        int(duration),
        int(resources),
        order
    )

    jobs.append(job)


# Sort by arrival time.
jobs.sort(
    key=lambda job: (job.arrival, job.order)
)

scheduler = Scheduler(w, jobs)

threads = []

for worker_id in range(w):

    thread = threading.Thread(
        target=scheduler.worker_run,
        args=(worker_id,)
    )

    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

# Output in job arrival/input order.
jobs.sort(key=lambda job: job.order)

total_waiting = 0

for job in jobs:

    waiting_time = job.start - job.arrival
    total_waiting += waiting_time

    print(
        job.job_id,
        f"W{job.worker}",
        job.start,
        job.finish
    )


average_wait = total_waiting / n

print(f"AVG_WAIT {average_wait:.2f}")
