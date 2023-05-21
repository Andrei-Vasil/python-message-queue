import datetime
import os
import time

BENCHMARKING = True
BENCHMARK_ID = 2
BENCHMARK_FILE = f'data/{datetime.date.today()}-{BENCHMARK_ID}.csv'

def mark_end_of_push(benchmark_id: str):
    if not BENCHMARKING:
        return
    os.system(f'echo {time.time()},{benchmark_id} >> {BENCHMARK_FILE}')

