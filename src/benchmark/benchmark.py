import datetime
import os
import time

BENCHMARKING = True
BENCHMARK_ID = 9
LATENCY_BENCHMARK_FILE = f'data/latency/{datetime.date.today()}-{BENCHMARK_ID}.csv'
PRODUCER_THROUGHPUT_BENCHMARK_FILE = f'data/throughput/producer/{datetime.date.today()}-{BENCHMARK_ID}.csv'
CONSUMER_THROUGHPUT_BENCHMARK_FILE = f'data/throughput/consumer/{datetime.date.today()}-{BENCHMARK_ID}.csv'

def mark_end_of_push(benchmark_id: str):
    if not BENCHMARKING:
        return
    os.system(f'echo {time.time()},{benchmark_id} >> {LATENCY_BENCHMARK_FILE}')

def count_producer_throughput():
    if not BENCHMARKING:
        return
    os.system(f'echo {int(time.time())} >> {PRODUCER_THROUGHPUT_BENCHMARK_FILE}')

def count_consumer_throughput():
    if not BENCHMARKING:
        return
    os.system(f'echo {int(time.time())} >> {CONSUMER_THROUGHPUT_BENCHMARK_FILE}')

