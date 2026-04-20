CREATE KEYSPACE IF NOT EXISTS test
WITH replication = {'class':'SimpleStrategy','replication_factor':3};

USE test;

CREATE TABLE IF NOT EXISTS sensor_data (
    device_id text,
    event_time timestamp,
    value double,
    PRIMARY KEY ((device_id), event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);