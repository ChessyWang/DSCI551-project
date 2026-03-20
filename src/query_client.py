from cassandra.cluster import Cluster
import time

cluster = Cluster(['cassandra1'])  # 连接种子节点
session = cluster.connect('test')

# 模拟写入 5 条数据
for i in range(5):
    session.execute(
        "INSERT INTO sensor_data (device_id, timestamp, value) VALUES (%s, %s, %s)",
        ('device1', int(time.time()*1000), f'value_{i}')
    )
    time.sleep(1)

print("Data inserted successfully.")