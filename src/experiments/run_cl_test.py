from db.cassandra_client import create_session
from benchmark.benchmark import run_workload
from utils import helper
import random
import time
from utils.path import get_results_path

CL_CSV_PATH = "cl_results.csv"

CONSISTENCY_LEVELS = ["QUORUM", "ONE"]

def generate_uniform_query_keys(num_devices, total_ops):
    per_device = total_ops // num_devices
    remainder = total_ops % num_devices

    query_keys = []

    for i in range(1, num_devices + 1):
        count = per_device + (1 if i <= remainder else 0)
        query_keys.extend([f"device_{i:03d}"] * count)

    random.shuffle(query_keys)
    return query_keys


def run_cl_experiment(session = None, num_devices = 100, total_ops = 5000):
    results = []
    cluster = None
    created_here = False

    if session is None:
        cluster, session = create_session(keyspace="test")
        created_here = True
        print("Created session for consistency-level experiment")

    time.sleep(5)
    # levels = CONSISTENCY_LEVELS[:]
    # random.shuffle(levels)
    # generate keys for query
    query_keys = generate_uniform_query_keys(num_devices, total_ops)

    try:
        # warm up
        # run_workload(
        #     session=session,
        #     workload_name="warmup",
        #     concurrency=10,
        #     total_ops=1000,
        #     write_ratio=0.0,
        #     num_devices=100,
        #     consistency="ONE",
        # )
        for cl in CONSISTENCY_LEVELS:
            print(f"\nRunning CL={cl}")
            result = run_workload(
                session=session,
                workload_name=f"cl_{cl}",
                concurrency=10,
                total_ops=total_ops,
                write_ratio=0.0,
                num_devices=num_devices,
                consistency=cl,
                query_keys=query_keys
            )

            result["experiment_type"] = "consistency_level"
            result["consistency_level"] = cl

            results.append(result)

        helper.write_results_to_csv(results, get_results_path(CL_CSV_PATH))
    finally:
        if created_here and cluster is not None:
            cluster.shutdown()
            print("Cluster connection closed in cl test.")


if __name__ == "__main__":
    run_cl_experiment()