import random
import csv
from query_client import query
from write_client import insert
def percentile(values, p):
    if not values:
        return 0.0
    values = sorted(values)
    k = int(len(values) * p / 100)
    k = min(k, len(values) - 1)
    return values[k]


def random_device_id(num_devices: int = 100):
    idx = random.randint(1, num_devices)
    return f"device_{idx}"

def write_results_to_csv(results, output_csv):
    if not results:
        return

    fieldnames = [
        "experiment_type",
        "workload_name",
        "replication_factor",
        "concurrency",
        "total_ops",
        "write_ratio",
        "read_ratio",
        "success_ops",
        "error_ops",
        "read_ops",
        "write_ops",
        "elapsed_sec",
        "throughput_ops_sec",
        "avg_latency_ms",
        "p95_latency_ms",
        "p99_latency_ms",
    ]

    write_header = False
    try:
        with open(output_csv, "r", newline="", encoding="utf-8"):
            pass
    except FileNotFoundError:
        write_header = True

    with open(output_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for row in results:
            writer.writerow(row)