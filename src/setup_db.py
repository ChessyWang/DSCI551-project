from cassandra_client import create_session

def run_cql(session, path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    statements = [stmt.strip() for stmt in content.split(";") if stmt.strip()]
    for stmt in statements:
        session.execute(stmt)
        print(f"===== execute statement: {stmt} ====== ")

if __name__ == "__main__":
    cluster, session = create_session()
    try:
        run_cql(session, "init.cql")
        print("---- finish database Setup ----")
    finally:
        cluster.shutdown()
