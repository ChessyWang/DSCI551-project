FROM cassandra:4.1

# 安装 Python 和依赖
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-dev build-essential libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# 创建虚拟环境
RUN python3 -m venv /opt/venv

# 激活 venv 并安装 cassandra-driver
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install cassandra-driver

# 拷贝初始化文件和应用脚本
COPY init.cql /init.cql
COPY src/ /app/

# 设置工作目录
WORKDIR /app

# 设置 PATH 使用虚拟环境
ENV PATH="/opt/venv/bin:$PATH"

# 启动 Cassandra 并初始化 schema
CMD bash -c "cassandra -f & sleep 30 && cqlsh -f /init.cql && tail -f /dev/null"