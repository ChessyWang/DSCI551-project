SCHEMAS = {
    "schema_a_no_bucket": {
        "drop": "DROP TABLE IF EXISTS test.sensor_data;",
        "create": """
            CREATE TABLE test.sensor_data (
                device_id text,
                event_time timestamp,
                value double,
                PRIMARY KEY ((device_id), event_time)
            ) WITH CLUSTERING ORDER BY (event_time DESC);
        """,
        "insert_mode": "no_bucket",
        "query_mode": "no_bucket",
        "description": "Partition by device_id only"
    },
    "schema_b_day_bucket": {
        "drop": "DROP TABLE IF EXISTS test.sensor_data;",
        "create": """
            CREATE TABLE test.sensor_data (
                device_id text,
                day_bucket date,
                event_time timestamp,
                value double,
                PRIMARY KEY ((device_id, day_bucket), event_time)
            ) WITH CLUSTERING ORDER BY (event_time DESC);
        """,
        "insert_mode": "day_bucket",
        "query_mode": "day_bucket",
        "description": "Partition by device_id + day_bucket"
    },
    "schema_c_region_hotspot": {
        "drop": "DROP TABLE IF EXISTS test.sensor_data;",
        "create": """
            CREATE TABLE test.sensor_data (
                region text,
                event_time timestamp,
                device_id text,
                value double,
                PRIMARY KEY ((region), event_time, device_id)
            ) WITH CLUSTERING ORDER BY (event_time DESC, device_id ASC);
        """,
        "insert_mode": "region",
        "query_mode": "region",
        "description": "Low-cardinality partition key: region"
    },
}
def get_schema(name):
    return SCHEMAS.get(name)