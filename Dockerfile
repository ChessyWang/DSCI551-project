FROM python:3.10-slim

# 安装 Cassandra Python driver
RUN pip install cassandra-driver

# 拷贝代码
COPY src/ /app/
WORKDIR /app

# 默认执行（你也可以后面 docker exec 手动跑）
CMD ["tail", "-f", "/dev/null"]