from cassandra_client import create_session
from query_client import query, query_recent
from write_client import insert, insert_sample_data


import time
import random

def single_write(session, consistency):
    device_id = "device_1"   # 或 random_device_id
    event_time = int(time.time() * 1000)
    value = round(random.uniform(10.0, 100.0), 2)

    insert(session, device_id, event_time, value, consistency)

def safe_read(session, consistency, num_ops=20):
    success = 0
    failure = 0
    latencies = []

    for _ in range(num_ops):
        try:
            start = time.perf_counter()

            rows = query(session, "device_1", limit=5, consistency=consistency)

            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)

            success += 1

        except Exception:
            failure += 1

    avg_latency = sum(latencies) / len(latencies) if latencies else 0

    print(f"\n[READ RESULT] CL={consistency}")
    print(f"Total: {num_ops}")
    print(f"Success: {success}")
    print(f"Failure: {failure}")
    print(f"Success Rate: {success/num_ops:.2%}")
    print(f"Avg Latency: {avg_latency:.2f} ms")


def safe_write(session, consistency, num_ops=50):
    success = 0
    failure = 0
    latencies = []

    for _ in range(num_ops):
        try:
            start = time.perf_counter()

            single_write(session, consistency)

            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)

            success += 1

        except Exception:
            failure += 1

    avg_latency = sum(latencies) / len(latencies) if latencies else 0

    print(f"\n[WRITE RESULT] CL={consistency}")
    print(f"Total: {num_ops}")
    print(f"Success: {success}")
    print(f"Failure: {failure}")
    print(f"Success Rate: {success/num_ops:.2%}")
    print(f"Avg Latency: {avg_latency:.2f} ms")

def print_cluster_status(session):
    hosts = session.cluster.metadata.all_hosts()

    up_hosts = []
    down_hosts = []

    print("\n=== Cluster Status ===")
    for host in hosts:
        status = "UP" if host.is_up else "DOWN"
        addr = getattr(host, "address", str(host))
        print(f"{addr} -> {status}")

        if host.is_up:
            up_hosts.append(host)
        else:
            down_hosts.append(host)

    print(f"Available nodes: {len(up_hosts)}")
    print(f"Down nodes: {len(down_hosts)}\n")

    return len(up_hosts), len(down_hosts)

def run_failure_test(session=None):
    print("Please stop one Cassandra node first, then run this test.\n")

    cluster = None
    created_here = False

    if session is None:
        cluster, session = create_session(keyspace="test")
        created_here = True
        print("Created session for failure test")

    try:
        up_nodes, down_nodes = print_cluster_status(session)

        if up_nodes >= 3:
            print("No node appears to be down yet. Stop one node first.\n")
            return

        print("Detected node failure. Running failure test...\n")

        safe_read(session, "QUORUM")
        safe_read(session, "ONE")

        safe_write(session, "QUORUM")
        safe_write(session, "ONE")

    finally:
        if created_here and cluster is not None:
            cluster.shutdown()
            print("Cluster connection closed in failure test.")


if __name__ == "__main__":
    run_failure_test()