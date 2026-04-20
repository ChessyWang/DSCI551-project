from cassandra_client import create_session, parse_consistency_level
from cassandra.query import SimpleStatement


def query(session, device_id: str, limit: int = 5, consistency: str = None):
    cql = """
    SELECT device_id, event_time, value
    FROM test.sensor_data
    WHERE device_id = %s
    LIMIT %s
    """
    if consistency is None:
        return list(session.execute(cql, (device_id, limit)))
    
    stmt = SimpleStatement(
        cql,
        consistency_level = parse_consistency_level(consistency)
    )
    return list(session.execute(stmt, (device_id, limit)))

def query_recent(session, device_id: str, limit: int = 5) -> None:
    rows = query(session, device_id, limit)
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