#!/bin/sh
set -e

echo "Waiting for 3 Cassandra nodes to be UN..."

until python /workspace/src/wait_for_cluster.py; do
  echo "Cluster not ready yet..."
  sleep 5
done

echo "Cluster is ready."
exec tail -f /dev/null