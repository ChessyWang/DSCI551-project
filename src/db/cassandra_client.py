from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra import ConsistencyLevel
import time
import os

def parse_consistency_level(level: str) -> int:
    level = level.upper()
    mapping = {
        "ONE": ConsistencyLevel.ONE,
        "QUORUM": ConsistencyLevel.QUORUM,
        "ALL": ConsistencyLevel.ALL
    }
    if level not in mapping:
        raise ValueError(f"Unsupported consistency level: {level}")
    return mapping[level]

def create_session(hosts=None, keyspace=None, max_retries=10, wait_seconds=5):
    if hosts is None:
        host_env = os.getenv("CASSANDRA_HOSTS")
        if host_env:
            hosts = [h.strip() for h in host_env.split(",")]
        else:
            hosts = ["127.0.0.1"]

    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            cluster = Cluster(hosts)
            session = cluster.connect()
            if keyspace:
                session.set_keyspace(keyspace)
            print(f"Connected to Cassandra on attempt {attempt}")
            return cluster, session
        except Exception as exc:
            last_error = exc
            print(f"Connection attempt {attempt} failed: {exc}")
            time.sleep(wait_seconds)

    raise RuntimeError(f"Could not connect to Cassandra: {last_error}")