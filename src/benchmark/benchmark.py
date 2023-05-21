import datetime
import os
import time

BENCHMARKING = True

benchmark_id = 2
benchmark_file = f'data/{datetime.date.today()}-{benchmark_id}.csv'

def mark_end_of_push(benchmark_id: str):
    if not BENCHMARKING:
        return
    os.system(f'echo {time.time()},{benchmark_id} >> {benchmark_file}')

