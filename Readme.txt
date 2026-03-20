Docker Hub: https://hub.docker.com/repository/docker/chessy2471/cassandra-cluster/general
Github: https://github.com/ChessyWang/DSCI551-project

Step:
1. run docker-compose build
1. docker-compose up -d, wait 30-60 seconds for starting
2. run docker exec -it cassandra1 cqlsh -f /init.cql to initialize schema
4. docker exec -it cassandra1 nodetool status
5. docker exec -it cassandra-app python3 write_client.py
6. docker exec -it cassandra-app python3 query_client.py
