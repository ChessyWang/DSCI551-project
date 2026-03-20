# Use official Cassandra image as base
FROM cassandra:4.1

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

    COPY init.cql /init.cql
    COPY src/ /app/

WORKDIR /app

CMD bash -c "cassandra -f & sleep 30 && cqlsh -f /init.cql && tail -f /dev/null"