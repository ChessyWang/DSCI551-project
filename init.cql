CREATE KEYSPACE IF NOT EXISTS test
WITH replication = {'class':'SimpleStrategy','replication_factor':2};

USE test;

CREATE TABLE IF NOT EXISTS sensor_data (
    device_id text,
    timestamp bigint,
    value text,
    PRIMARY KEY (device_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);