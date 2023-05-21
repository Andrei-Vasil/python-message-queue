import datetime
import os
import time

BENCHMARKING = True

benchmark_id = 1
benchmark_file = f'data/{datetime.date.today()}-{benchmark_id}.csv'

def mark_end_of_push(benchmark_id: str):
    if not BENCHMARKING:
        return
    pid = os.fork()
    if pid == 0:
        __write_timestamp_to_file(time.time(), benchmark_id, benchmark_file)
        exit(0)

def __write_timestamp_to_file(timestamp: float, benchmark_id: str, file_path: str):
    os.system(f'echo {timestamp},{benchmark_id} >> {file_path}')
