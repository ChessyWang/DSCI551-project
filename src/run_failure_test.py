from cassandra_client import create_session
from query_client import query_recent
from write_client import insert_sample_data


def safe_read(session, consistency):
    try:
        result = query_recent(session, "device_1", limit=5, consistency=consistency)
        print(f"\n[READ SUCCESS] CL={consistency}")
        print(f"Rows returned: {len(result)}")
        print(f"Latency: {result['latency_ms']:.2f} ms")
    except Exception as exc:
        print(f"\n[READ FAILED] CL={consistency}")
        print(exc)


def safe_write(session, consistency):
    try:
        result = insert_sample_data(session, num_rows=100, consistency=consistency)
        print(f"\n[WRITE RESULT] CL={consistency}")
        # print(f"Success: {result['success']}")
        # print(f"Failure: {result['failure']}")
        # print(f"Average latency: {result['avg_latency_ms']:.2f} ms")
    except Exception as exc:
        print(f"\n[WRITE FAILED] CL={consistency}")
        print(exc)

def run_failure_test():
    print("Run this after stopping one Cassandra node.\n")

    cluster, session = create_session(keyspace="test")
    try:
        safe_read(session, "ONE")
        safe_read(session, "QUORUM")

        safe_write(session, "ONE")
        safe_write(session, "QUORUM")
    finally:
        cluster.shutdown()


if __name__ == "__main__":
    run_failure_test()