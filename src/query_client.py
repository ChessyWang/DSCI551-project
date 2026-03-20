from cassandra.cluster import Cluster

cluster = Cluster(['cassandra1'])
session = cluster.connect('test')

rows = session.execute(
    "SELECT * FROM sensor_data WHERE device_id=%s ORDER BY timestamp DESC LIMIT 5",
    ('device1',)
)

print("Query results:")

for row in rows:
    print(row)