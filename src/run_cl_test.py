from cassandra_client import create_session
from benchmark import run_workload
import helper

CONSISTENCY_LEVELS = ["ONE", "QUORUM"]


def run_cl_experiment():
    results = []

    for cl in CONSISTENCY_LEVELS:
        print(f"\nRunning CL={cl}")

        cluster, session = create_session(keyspace="test")

        try:
            result = run_workload(
                session=session,
                workload_name=f"cl_{cl}",
                concurrency=10,
                total_ops=1000,
                write_ratio=0.8,
                num_devices=100,
                consistency=cl,
            )

            result["experiment_type"] = "consistency_level"
            result["consistency_level"] = cl

            results.append(result)

        finally:
            cluster.shutdown()

    helper.write_results_to_csv(results, "cl_results.csv")


if __name__ == "__main__":
    run_cl_experiment()