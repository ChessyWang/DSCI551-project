Docker Hub: https://hub.docker.com/repository/docker/chessy2471/cassandra-cluster/general
Github: https://github.com/ChessyWang/DSCI551-project

====================currently in use======================
Step：pull official mirror +install dependencies
1. docker-compose up -d
2. pip install -r requirements.txt
3. python src/setup_db.py
4. python src/write_client.py
5. python src/query_client.py 
==========================================================

=======================deprecated=========================
Step:
1. run docker-compose build（Dockerfile）
2. docker-compose up -d, wait 30-60 seconds for starting
3. run docker exec -it cassandra1 cqlsh -f /init.cql to initialize schema
4. docker exec -it cassandra1 nodetool status
5. docker exec -it cassandra-app python3 write_client.py
6. docker exec -it cassandra-app python3 query_client.py
==========================================================

File Structure
project/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── init.cql
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── cassandra_client.py
│   ├── setup_db.py
│   ├── writer.py
│   ├── reader.py
│   ├── metrics.py
│   └── cluster_info.py
│
├── experiments/
│   ├── __init__.py
│   ├── run_insert_benchmark.py
│   ├── run_query_benchmark.py
│   ├── run_cl_comparison.py
│   └── run_failure_test.py
│
├── data/
│   └── sample_events.csv
│
├── results/
│   └── metrics.csv
│
└── scripts/
    ├── start_cluster.sh
    ├── load_schema.sh
    └── demo_flow.sh