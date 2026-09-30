"""
Q9 - Threaded Job Scheduler Simulation

Interpretation used for the assignment:
The statement supplies a resource count per job but does not specify worker
resource capacities. Therefore each worker executes one job at a time; the
resource count is validated and retained as job metadata, but does not limit
assignment. Jobs are selected by highest priority, then earliest arrival.
Python 3.10+
"""
from dataclasses import dataclass
from queue import PriorityQueue
from threading import Lock, Thread
import heapq

@dataclass
class Job:
    arrival: int
    job_id: str
    priority: int
    duration: int
    resources: int
    sequence: int
    start: int = -1
    finish: int = -1
    worker: int = -1

def simulate(workers, jobs):
    # Event heap: (finish_time, worker_id)
    available = list(range(1, workers + 1))
    heapq.heapify(available)

    jobs_sorted = sorted(jobs, key=lambda j: (j.arrival, j.sequence))
    waiting = []
    events = []
    result = []

    i = 0
    time = 0

    while i < len(jobs_sorted) or waiting or events:
        if not waiting and not events and i < len(jobs_sorted):
            time = max(time, jobs_sorted[i].arrival)

        while i < len(jobs_sorted) and jobs_sorted[i].arrival <= time:
            job = jobs_sorted[i]
            # Higher priority first; for ties earlier arrival, then input order.
            heapq.heappush(waiting, (-job.priority, job.arrival, job.sequence, job))
            i += 1

        # Complete all workers available at the current time.
        while events and events[0][0] <= time:
            finish, worker_id = heapq.heappop(events)
            heapq.heappush(available, worker_id)

        while available and waiting:
            _, _, _, job = heapq.heappop(waiting)
            worker_id = heapq.heappop(available)
            job.start = time
            job.finish = time + job.duration
            job.worker = worker_id
            result.append(job)
            heapq.heappush(events, (job.finish, worker_id))

        if events:
            # Advance simulated time to the next worker completion.
            # If more jobs arrive first, the loop will enqueue them at that time.
            next_arrival = jobs_sorted[i].arrival if i < len(jobs_sorted) else float("inf")
            time = min(events[0][0], next_arrival)
        elif i < len(jobs_sorted):
            time = max(time, jobs_sorted[i].arrival)

    return result

def main():
    w, n = map(int, input().split())
    if not (1 <= w <= 64 and 1 <= n <= 200000):
        raise ValueError("Invalid worker/job count.")

    jobs = []
    for seq in range(n):
        arrival, job_id, priority, duration, resources = input().split()
        job = Job(
            int(arrival), job_id, int(priority), int(duration),
            int(resources), seq
        )
        if job.arrival < 0 or job.duration <= 0 or job.resources <= 0:
            raise ValueError("Invalid job fields.")
        jobs.append(job)

    finished = simulate(w, jobs)

    # Report in actual execution/start order.
    for job in sorted(finished, key=lambda j: (j.start, j.worker, j.sequence)):
        print(job.job_id, f"W{job.worker}", job.start, job.finish)

    avg_wait = sum(job.start - job.arrival for job in finished) / n
    print(f"AVG_WAIT {avg_wait:.2f}")

if __name__ == "__main__":
    main()
