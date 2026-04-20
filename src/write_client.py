import random
from datetime import datetime, timedelta
from cassandra_client import create_session, parse_consistency_level
from cassandra.query import SimpleStatement
from schemas import SCHEMAS

def insert_row_by_schema(session, schema_name, device_id, event_time, value, region=None):
    schema = SCHEMAS[schema_name]
    mode = schema["insert_mode"]

    if mode == "no_bucket":
        cql = """
        INSERT INTO test.sensor_data (device_id, event_time, value)
        VALUES (%s, %s, %s)s
        """
        session.execute(cql, (device_id, event_time, value))

    elif mode == "day_bucket":
        cql = """
        INSERT INTO test.sensor_data (device_id, day_bucket, event_time, value)
        VALUES (%s, %s, %s, %s)
        """
        session.execute(cql, (device_id, event_time.date(), event_time, value))

    elif mode == "region":
        cql = """
        INSERT INTO test.sensor_data (region, event_time, device_id, value)
        VALUES (%s, %s, %s, %s)
        """
        session.execute(cql, (region, event_time, device_id, value))


def insert(session, device_id: str, event_time, value: float, consistency: str = None) -> None:
    cql = """
    INSERT INTO test.sensor_data (device_id, event_time, value)
    VALUES (%s, %s, %s)
    """
    if consistency is None:
        session.execute(cql, (device_id, event_time, value))
        return
    
    stmt = SimpleStatement(
        cql,
        consistency_level=parse_consistency_level(consistency)
    )
    session.execute(stmt, (device_id, event_time, value))


def insert_sample_data(session, num_rows: int = 10) -> None:
    now = datetime.utcnow()
    for i in range(num_rows):
        device_id = f"device_{random.randint(1, 3)}"
        event_time = now + timedelta(seconds=i)
        value = round(random.uniform(10, 100), 2)
        insert(session, device_id, event_time, value)


if __name__ == "__main__":
    cluster, session = create_session(keyspace="test")
    try:
        insert_sample_data(session, num_rows=10)
        print("Sample data inserted.")
    finally:
        cluster.shutdown()