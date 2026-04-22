from cassandra_client import create_session, parse_consistency_level
from cassandra.query import SimpleStatement
from schemas import SCHEMAS
from datetime import datetime, timedelta
def query_range(session, schema_name, device_id, start_time, end_time, region=None):
    schema = SCHEMAS[schema_name]
    mode = schema["query_mode"]

    if mode == "no_bucket":
        cql = """
        SELECT device_id, event_time, value
        FROM test.sensor_dataa
        WHERE device_id = %s
          AND event_time >= %s
          AND event_time <= %s
        """
        return list(session.execute(cql, (device_id, start_time, end_time)))

    elif mode == "day_bucket":
        # single-day bucket range query
        cql = """
        SELECT device_id, day_bucket, event_time, value
        FROM test.sensor_datab
        WHERE device_id = %s
          AND day_bucket = %s
          AND event_time >= %s
          AND event_time <= %s
        """
        return list(session.execute(cql, (device_id, start_time.date(), start_time, end_time)))

    elif mode == "region":
        cql = """
        SELECT region, event_time, device_id, value
        FROM test.sensor_datac
        WHERE region = %s
          AND event_time >= %s
          AND event_time <= %s
        """
        return list(session.execute(cql, (region, start_time, end_time)))
    
def query_by_schema(session, schema_name, device_id, limit=5, region=None):
    schema = SCHEMAS[schema_name]
    mode = schema["query_mode"]

    if mode == "no_bucket":
        cql = f"""
        SELECT device_id, event_time, value
        FROM test.sensor_dataa
        WHERE device_id = %s
        LIMIT {limit}
        """
        return list(session.execute(cql, (device_id,)))

    elif mode == "day_bucket":
        # query recent data only for today bucket
        day_bucket = datetime.utcnow().date()
        cql = f"""
        SELECT device_id, day_bucket, event_time, value
        FROM test.sensor_datab
        WHERE device_id = %s AND day_bucket = %s
        LIMIT {limit}
        """
        return list(session.execute(cql, (device_id, day_bucket)))

    elif mode == "region":
        cql = f"""
        SELECT region, event_time, device_id, value
        FROM test.sensor_datac
        WHERE region = %s
        LIMIT {limit}
        """
        return list(session.execute(cql, (region,)))
    

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

def query_recent(session, device_id: str, limit: int = 5, consistency: str = None):
    rows = query(session, device_id, limit, consistency=consistency)
    if not rows:
        print("No rows found.")
    else:
        for row in rows:
            print(row)

    return rows


if __name__ == "__main__":
    cluster, session = create_session(keyspace="test")
    try:
        query_recent(session, "device_1", limit=5, consistency="ONE")
    finally:
        cluster.shutdown()