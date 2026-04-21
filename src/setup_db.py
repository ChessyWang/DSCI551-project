from cassandra_client import create_session
from recreate_client import delete_all
def run_cql(session, path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    statements = [stmt.strip() for stmt in content.split(";") if stmt.strip()]
    for stmt in statements:
        session.execute(stmt)
        print(f"===== execute statement: {stmt} ====== ")

def setup():
    cluster, session = create_session()
    try:
        delete_all(session)
        run_cql(session, "init.cql")
        print("---- finish database Setup ----")
    finally:
        cluster.shutdown()

