import random
from datetime import datetime, timedelta
from cassandra_client import create_session

    
def insert(session, device_id: str, event_time, value: float) -> None:
    cql = """
    INSERT INTO test.sensor_data (device_id, event_time, value)
    VALUES (%s, %s, %s)
    """
    session.execute(cql, (device_id, event_time, value))


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