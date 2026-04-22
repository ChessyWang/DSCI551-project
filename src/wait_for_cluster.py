from cassandra.cluster import Cluster
import os
import sys
import time

hosts = os.getenv("CASSANDRA_HOSTS", "cassandra1,cassandra2,cassandra3").split(",")

REQUIRED_UP = 3
REQUIRED_STABLE_ROUNDS = 3
CHECK_INTERVAL = 3
MAX_ATTEMPTS = 20

stable_rounds = 0

for attempt in range(1, MAX_ATTEMPTS + 1):
    cluster = None
    try:
        cluster = Cluster(hosts)
        session = cluster.connect()
        hosts_meta = session.cluster.metadata.all_hosts()

        up_hosts = [h for h in hosts_meta if h.is_up]
        up_count = len(up_hosts)

        print(f"[Attempt {attempt}] up hosts = {up_count}")

        if up_count >= REQUIRED_UP:
            stable_rounds += 1
            print(f"Stable rounds: {stable_rounds}/{REQUIRED_STABLE_ROUNDS}")
        else:
            stable_rounds = 0

        if stable_rounds >= REQUIRED_STABLE_ROUNDS:
            sys.exit(0)

    except Exception as e:
        print(f"[Attempt {attempt}] cluster check failed: {e}")
        stable_rounds = 0

    finally:
        if cluster is not None:
            cluster.shutdown()

    time.sleep(CHECK_INTERVAL)

sys.exit(1)