Github: https://github.com/ChessyWang/DSCI551-project

====================currently in use======================
Step：pull official mirror + install dependencies
make sure you have enough memory to start all 3 replication nodes
1. docker-compose up -d
2. docker exec -it cassandra1 nodetool status
# wait until all 3 nodes are UN
3. docker exec -it cassandra-app bash to enter docker container
4. pip install -r requirements.txt
5. python src/main.py to show main menu
select an area to test

==========================================================
