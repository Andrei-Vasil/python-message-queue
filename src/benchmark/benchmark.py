import datetime
import os
import time

BENCHMARKING = False

def mark_end_of_push(benchmark_id: str, scenario_id: str):
    if not BENCHMARKING:
        return
    os.system(f'echo {time.time()},{benchmark_id} >> data/latency/{scenario_id}.csv')

def count_producer_throughput(scenario_id: str):
    if not BENCHMARKING:
        return
    os.system(f'echo {int(time.time())} >> data/throughput/producer/{scenario_id}.csv')

def count_consumer_throughput(scenario_id: str):
    if not BENCHMARKING:
        return
    os.system(f'echo {int(time.time())} >> data/throughput/consumer/{scenario_id}.csv')

