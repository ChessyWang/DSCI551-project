
from .schemas import SCHEMAS
def recreate_keyspace(session, rf=2, KEYSPACE="test"):
    session.execute(f"DROP KEYSPACE IF EXISTS {KEYSPACE}")
    session.execute(f"""
        CREATE KEYSPACE {KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': {rf}}}
    """)
    session.set_keyspace(KEYSPACE)


def recreate_schema(session, schema_name):
    schema = SCHEMAS[schema_name]
    session.execute(schema["drop"])
    session.execute(schema["create"])
    print(f"Created schema: {schema_name}")

def delete_all(session):
    session.execute("DROP KEYSPACE IF EXISTS test")