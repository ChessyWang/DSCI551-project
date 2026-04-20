import helper
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean
from cassandra_client import create_session
from helper import percentile

def run_single_op(session, write_ratio: float, num_devices: int):
    """
    write_ratio = 0.8 means 80% writes, 20% reads
    """
    start = time.perf_counter()
    success = 1

    try:
        device_id = helper.random_device_id(num_devices)

        if random.random() < write_ratio:
            event_time = int(time.time() * 1000)
            value = round(random.uniform(10.0, 100.0), 2)
            helper.insert(session, device_id, event_time, value)
            op_type = "write"
        else:
            helper.query(session, device_id, limit=5)
            op_type = "read"

    except Exception as e:
        success = 0
        op_type = "error"

    latency_ms = (time.perf_counter() - start) * 1000
    return {
        "success": success,
        "latency_ms": latency_ms,
        "op_type": op_type,
    }




# -----------------------------
# Benchmark Core
# -----------------------------
def run_workload(
    session,
    workload_name: str,
    concurrency: int,
    total_ops: int,
    write_ratio: float,
    num_devices: int = 100,
):
    """
    Run one benchmark round.
    """
    latencies = []
    success_count = 0
    read_count = 0
    write_count = 0
    error_count = 0

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(run_single_op, session, write_ratio, num_devices)
            for _ in range(total_ops)
        ]

        for future in as_completed(futures):
            result = future.result()
            latencies.append(result["latency_ms"])

            if result["success"]:
                success_count += 1
            else:
                error_count += 1

            if result["op_type"] == "read":
                read_count += 1
            elif result["op_type"] == "write":
                write_count += 1

    elapsed = time.perf_counter() - start_time
    throughput = success_count / elapsed if elapsed > 0 else 0.0

    return {
        "workload_name": workload_name,
        "concurrency": concurrency,
        "total_ops": total_ops,
        "write_ratio": write_ratio,
        "read_ratio": 1 - write_ratio,
        "success_ops": success_count,
        "error_ops": error_count,
        "read_ops": read_count,
        "write_ops": write_count,
        "elapsed_sec": elapsed,
        "throughput_ops_sec": throughput,
        "avg_latency_ms": mean(latencies) if latencies else 0.0,
        "p95_latency_ms": percentile(latencies, 95),
        "p99_latency_ms": percentile(latencies, 99),
    }


# -----------------------------
# Experiment Suites
# -----------------------------
def workload_intensity_experiment(session, output_csv: str):
    """
    Compare different workload intensities.
    Keep RF fixed outside this script.
    """
    configs = [
        {"workload_name": "low", "concurrency": 2, "total_ops": 200, "write_ratio": 1.0},
        {"workload_name": "medium", "concurrency": 5, "total_ops": 500, "write_ratio": 1.0},
        {"workload_name": "high", "concurrency": 10, "total_ops": 1000, "write_ratio": 1.0},
        {"workload_name": "very_high", "concurrency": 20, "total_ops": 2000, "write_ratio": 1.0},
    ]

    results = []
    for cfg in configs:
        print(f"Running intensity workload: {cfg}")
        result = run_workload(session=session, **cfg)
        result["experiment_type"] = "workload_intensity"
        result["replication_factor"] = "manual_set"
        results.append(result)

    helper.write_results_to_csv(results, output_csv)


def read_write_mix_experiment(session, output_csv: str):
    """
    Compare different read/write ratios.
    """
    configs = [
        {"workload_name": "write_only", "concurrency": 10, "total_ops": 1000, "write_ratio": 1.0},
        {"workload_name": "mixed_80_20", "concurrency": 10, "total_ops": 1000, "write_ratio": 0.8},
        {"workload_name": "mixed_50_50", "concurrency": 10, "total_ops": 1000, "write_ratio": 0.5},
    ]

    results = []
    for cfg in configs:
        print(f"Running mix workload: {cfg}")
        result = run_workload(session=session, **cfg)
        result["experiment_type"] = "read_write_mix"
        result["replication_factor"] = "manual_set"
        results.append(result)

    helper.write_results_to_csv(results, output_csv)


def replication_factor_experiment(session, output_csv: str, rf_label: int):
    """
    Run the SAME workload after you manually recreate the keyspace with RF=1/2/3.
    """
    configs = [
        {"workload_name": "rf_compare", "concurrency": 10, "total_ops": 1000, "write_ratio": 0.8},
    ]

    results = []
    for cfg in configs:
        print(f"Running RF={rf_label} workload: {cfg}")
        result = run_workload(session=session, **cfg)
        result["experiment_type"] = "replication_factor"
        result["replication_factor"] = rf_label
        results.append(result)

    helper.write_results_to_csv(results, output_csv)



# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    cluster, session = create_session(keyspace="test")

    try:
        # 1) workload intensity comparison
        workload_intensity_experiment(session, "results.csv")

        # 2) read/write mix comparison
        read_write_mix_experiment(session, "results.csv")

        # 3) replication factor comparison
        # IMPORTANT:
        # Run this script multiple times after manually changing RF in keyspace.
        # Example:
        #   first run with RF=1  -> replication_factor_experiment(..., rf_label=1)
        #   second run with RF=2 -> replication_factor_experiment(..., rf_label=2)
        #   third run with RF=3  -> replication_factor_experiment(..., rf_label=3)
        # replication_factor_experiment(session, "results.csv", rf_label=2)

    finally:
        cluster.shutdown()