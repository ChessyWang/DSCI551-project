from cassandra_client import create_session


def query_recent(session, device_id: str, limit: int = 5) -> None:
    query_cql = """
    SELECT device_id, event_time, value
    FROM test.sensor_data
    WHERE device_id = %s
    LIMIT %s
    """

    rows = session.execute(query_cql, (device_id, limit))

    print(f"Recent records for {device_id}:")
    found = False
    for row in rows:
        found = True
        print(row)

    if not found:
        print("No rows found.")


if __name__ == "__main__":
    cluster, session = create_session(keyspace="test")
    try:
        query_recent(session, "device_1", limit=5)
    finally:
        cluster.shutdown()