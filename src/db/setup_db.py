from pathlib import Path
from .cassandra_client import create_session
from .recreate_client import delete_all
from benchmark.benchmark_schema import preload_data
from .schemas import SCHEMAS

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
        cql_path = Path(__file__).resolve().parents[2] / "init.cql"
        run_cql(session, str(cql_path))
        # run_cql(session, "init.cql")
        for schema_name in SCHEMAS:
            preload_data(session, schema_name, num_rows=3000, num_devices=100)
        print("---- finish database Setup ----")
    finally:
        cluster.shutdown()

