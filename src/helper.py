import random
import csv
from query_client import query
from write_client import insert
from datetime import datetime, timedelta
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


def random_region():
    return random.choice(["west", "east", "north"])


def random_event_time(day_span=7):
    now = datetime.utcnow()
    delta_days = random.randint(0, day_span - 1)
    delta_seconds = random.randint(0, 24 * 3600 - 1)
    return now - timedelta(days=delta_days, seconds=delta_seconds)


# def write_results_to_csv(results, output_csv):
#     if not results:
#         return

#     fieldnames = [
#         "experiment_type",
#         "consistency_level",
#         "workload_name",
#         "replication_factor",
#         "concurrency",
#         "total_ops",
#         "write_ratio",
#         "read_ratio",
#         "success_ops",
#         "error_ops",
#         "read_ops",
#         "write_ops",
#         "elapsed_sec",
#         "throughput_ops_sec",
#         "avg_latency_ms",
#         "p95_latency_ms",
#         "p99_latency_ms",
#     ]

#     write_header = False
#     try:
#         with open(output_csv, "r", newline="", encoding="utf-8"):
#             pass
#     except FileNotFoundError:
#         write_header = True

#     with open(output_csv, "a", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         if write_header:
#             writer.writeheader()
#         for row in results:
#             writer.writerow(row)

def write_results_to_csv(results, csv_file):
    if not results:
        return

    fieldnames = list(results[0].keys())

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)