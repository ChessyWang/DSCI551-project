CREATE KEYSPACE IF NOT EXISTS test
WITH replication = {'class':'SimpleStrategy','replication_factor':3};

USE test;

CREATE TABLE IF NOT EXISTS sensor_data (
    device_id text,
    event_time timestamp,
    value double,
    PRIMARY KEY ((device_id), event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

 CREATE TABLE test.sensor_dataa (
                device_id text,
                event_time timestamp,
                value double,
                PRIMARY KEY ((device_id), event_time)
            ) WITH CLUSTERING ORDER BY (event_time DESC);

CREATE TABLE test.sensor_datab (
                device_id text,
                day_bucket date,
                event_time timestamp,
                value double,
                PRIMARY KEY ((device_id, day_bucket), event_time)
            ) WITH CLUSTERING ORDER BY (event_time DESC);

CREATE TABLE test.sensor_datac (
                region text,
                event_time timestamp,
                device_id text,
                value double,
                PRIMARY KEY ((region), event_time, device_id)
            ) WITH CLUSTERING ORDER BY (event_time DESC, device_id ASC);