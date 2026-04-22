from pathlib import Path
import csv
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
from datetime import datetime
from .path import DATA_DIR

CSV_PATH = DATA_DIR / "sample_sensor_data.csv"

def load_csv_if_empty(session, filename=CSV_PATH):
    row = session.execute("SELECT device_id FROM sensor_data LIMIT 1").one()
    if row is not None:
        print("Data already exists, skipping CSV load.")
        return

    if not Path(filename).exists():
        raise FileNotFoundError(f"CSV file not found: {filename}")

    print(f"Loading data from {filename}...")

    insert_stmt = session.prepare(
        "INSERT INTO sensor_data (device_id, event_time, value) VALUES (?, ?, ?)"
    )

    batch = BatchStatement(consistency_level=ConsistencyLevel.ONE)
    count = 0

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            device_id = row["device_id"]
            event_time = datetime.fromisoformat(row["event_time"])
            value = float(row["value"])

            batch.add(insert_stmt, (device_id, event_time, value))
            count += 1

            if count % 50 == 0:
                session.execute(batch)
                batch.clear()

    if len(batch) > 0:
        session.execute(batch)

    print(f"Loaded {count} records from CSV.")