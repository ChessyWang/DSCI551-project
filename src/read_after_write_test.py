import time
import random
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

def write_sensor(session, device_id, value, cl):
    stmt = SimpleStatement(
        "INSERT INTO sensor_data (device_id, event_time, value) VALUES (%s, toTimestamp(now()), %s)",
        consistency_level=cl
    )
    session.execute(stmt, (device_id, value))

def read_latest(session, device_id, cl):
    stmt = SimpleStatement(
        "SELECT value, event_time FROM sensor_data WHERE device_id = %s LIMIT 1",
        consistency_level=cl
    )
    result = session.execute(stmt, (device_id,))
    return list(result)

def read_after_write_test(session, device_id, cl_write, cl_read, write_label, read_label, rounds=5):
    # print("DEBUG write cl:", cl_write, type(cl_write))
    # print("DEBUG read cl:", cl_read, type(cl_read))
    print(f"\nTesting Read-After-Write with WRITE={write_label}, READ={read_label}")

    success = 0

    for i in range(rounds):
        value = round(random.uniform(10, 100), 2)

        write_sensor(session, device_id, value, cl_write)
        rows = read_latest(session, device_id, cl_read)

        if rows and rows[0].value == value:
            # print(f"[Round {i+1}] ✅ Fresh read")
            success += 1
        else:
            got = rows[0].value if rows else None
            print(f"[Round {i+1}] ❌ Stale read (wrote {value}, got {got})")

    print(f"Fresh reads: {success}/{rounds}")

def run_consistency_demo(session, rounds):
    device_id = "device_1"

    print("\n=== Consistency Demo: Read After Write ===")

    read_after_write_test(
        session,
        device_id,
        ConsistencyLevel.ONE,
        ConsistencyLevel.ONE,
        "ONE",
        "ONE",
        rounds
    )

    read_after_write_test(
        session,
        device_id,
        ConsistencyLevel.QUORUM,
        ConsistencyLevel.QUORUM,
        "QUORUM",
        "QUORUM",
        rounds
    )