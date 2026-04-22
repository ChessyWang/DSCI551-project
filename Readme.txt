Docker Hub: https://hub.docker.com/repository/docker/chessy2471/cassandra-cluster/general
Github: https://github.com/ChessyWang/DSCI551-project

====================currently in use======================
Step：pull official mirror +install dependencies
1. docker-compose up -d
2. docker exec -it cassandra1 nodetool status
# wait until all 3 nodes are UN
3. docker exec -it cassandra-app bash
4. pip install -r requirements.txt
5. python src/main.py to show main menu
select an area to test

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