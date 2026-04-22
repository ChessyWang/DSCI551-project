import csv
import random
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean
import helper
import query_client
import write_client 
from db.schemas import SCHEMAS
from db.cassandra_client import create_session
from plot_schema_results import plot_schema_results

KEYSPACE = "test"
RESULT_CSV = "schema_results.csv"


def preload_data(session, schema_name, num_rows=5000, num_devices=100):
    print(f"Preloading {num_rows} rows for {schema_name} ...")
    for _ in range(num_rows):
        device_id = helper.random_device_id(num_devices)
        event_time = helper.random_event_time(day_span=7)
        value = round(random.uniform(10.0, 100.0), 2)
        region = helper.random_region()
        write_client.insert_row_by_schema(session, schema_name, device_id, event_time, value, region=region)
    print("Preload finished.")


# =========================================================
# Workload Runner
# =========================================================
def run_single_operation(session, schema_name, read_ratio=0.2, num_devices=100):
    start = time.perf_counter()
    success = 1
    op_type = "unknown"

    try:
        device_id = helper.random_device_id(num_devices)
        region = helper.random_region()

        if random.random() < (1 - read_ratio):
            op_type = "write"
            event_time = datetime.utcnow()
            value = round(random.uniform(10.0, 100.0), 2)
            write_client.insert_row_by_schema(session, schema_name, device_id, event_time, value, region=region)

        else:
            if random.random() < 0.5:
                op_type = "recent_read"
                query_client.query_by_schema(session, schema_name, device_id, limit=5, region=region)
            else:
                op_type = "range_read"
                end_time = datetime.utcnow()
                start_time = end_time - timedelta(hours=6)
                query_client.query_range(session, schema_name, device_id, start_time, end_time, region=region)

    except Exception as e:
        success = 0
        op_type = "error"

    latency_ms = (time.perf_counter() - start) * 1000
    return {
        "success": success,
        "op_type": op_type,
        "latency_ms": latency_ms
    }


def run_benchmark(session, schema_name, concurrency=10, total_ops=1000, read_ratio=0.2):
    latencies = []
    success_ops = 0
    write_ops = 0
    recent_read_ops = 0
    range_read_ops = 0
    error_ops = 0

    t0 = time.perf_counter()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(run_single_operation, session, schema_name, read_ratio)
            for _ in range(total_ops)
        ]

        for future in as_completed(futures):
            result = future.result()
            latencies.append(result["latency_ms"])

            if result["success"]:
                success_ops += 1
            else:
                error_ops += 1

            if result["op_type"] == "write":
                write_ops += 1
            elif result["op_type"] == "recent_read":
                recent_read_ops += 1
            elif result["op_type"] == "range_read":
                range_read_ops += 1

    elapsed = time.perf_counter() - t0
    throughput = success_ops / elapsed if elapsed > 0 else 0.0

    return {
        "schema_name": schema_name,
        "schema_description": SCHEMAS[schema_name]["description"],
        "concurrency": concurrency,
        "total_ops": total_ops,
        "read_ratio": read_ratio,
        "write_ratio": 1 - read_ratio,
        "success_ops": success_ops,
        "error_ops": error_ops,
        "write_ops": write_ops,
        "recent_read_ops": recent_read_ops,
        "range_read_ops": range_read_ops,
        "elapsed_sec": elapsed,
        "throughput_ops_sec": throughput,
        "avg_latency_ms": mean(latencies) if latencies else 0.0,
        "p95_latency_ms": helper.percentile(latencies, 95),
        "p99_latency_ms": helper.percentile(latencies, 99),
    }



# =========================================================
# Experiment Driver
# =========================================================
def run_schema_exploration(session):
    results = []

    experiment_configs = [
        {"concurrency": 5, "total_ops": 500, "read_ratio": 0.2},
        {"concurrency": 10, "total_ops": 1000, "read_ratio": 0.2},
        {"concurrency": 20, "total_ops": 2000, "read_ratio": 0.2},
    ]

    for schema_name in SCHEMAS:

        for cfg in experiment_configs:
            print(f"Running {schema_name} with config {cfg}")
            result = run_benchmark(session, schema_name, **cfg)
            results.append(result)

    helper.write_results_to_csv(results, RESULT_CSV)
    print(f"Results written to {RESULT_CSV}")

def test_run_schema_exploration(session):
    cluster, session = create_session()
    try:
        # for schema_name in SCHEMAS:
        #     preload_data(session, schema_name, num_rows=3000, num_devices=100)
        # recreate_client.recreate_keyspace(session, rf=2, KEYSPACE=KEYSPACE)
        run_schema_exploration(session)

    finally:
        plot_schema_results()
        # recreate_client.delete_all(session)
        # cluster.shutdown()

if __name__ == "__main__":
    test_run_schema_exploration(session=None)