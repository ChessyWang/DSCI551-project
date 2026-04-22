import sys
from setup_db import setup
from run_cl_test import run_cl_experiment
from run_failure_test import run_failure_test
from plot_results import plot_consistency_level
from write_client import insert_sample_data
from cassandra_client import create_session
from query_client import query_recent

def simulate_device_ingestion(session):
    print("\n=== Data Ingestion ===")
    print("Simulating devices sending sensor data to Cassandra...\n")

    insert_sample_data(session, num_rows=10000, num_devices = 100, consistency="ONE")
    print("Data ingestion completed.\n")


def query_recent_readings(session):
    print("\n=== Query Recent Data ===")
    print("Fetching latest sensor readings for device_1...\n")

    query_recent(session, "device_1", limit=5, consistency="ONE")
    print("Query completed.\n")


def compare_consistency_modes(session = None):
    print("\n=== Consistency Mode Comparison ===")
    print("Comparing performance under different consistency levels (ONE vs QUORUM)...\n")

    run_cl_experiment(session)

    print("\nConsistency comparison finished.\n")


def simulate_node_failure(session=None):
    print("\n=== Node Failure Simulation ===")
    print("Simulating failure of one Cassandra node and observing system behavior...\n")

    run_failure_test(session)

    print("\nFailure simulation finished.\n")

#Todo: schema + workload test


def print_menu():
    print("\n==============================")
    print(" Distributed IoT Data Platform ")
    print("==============================")
    print("1. Ingest sensor data")
    print("2. Query recent readings")
    print("3. Analyze partition key impact")
    print("4. Compare consistency modes")
    print("5. Performance Under Load")
    print("6. Simulate node failure")
    print("7. Exit")
    print("==============================")


def main():
    try:
        setup()
    except Exception as e:
        print("Setup failed:", e)
        print("Make sure Cassandra cluster is ready.\n")
    
    try: 
        cluster, session = create_session(keyspace="test")

        while True:
            print_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                simulate_device_ingestion(session)

            elif choice == "2":
                query_recent_readings(session)
            
            elif choice == "3":
                #todo: schema test
                print("test schema")
            
            elif choice == "4":
                compare_consistency_modes(session)
                ans = input("Plot results now? (y/n): ").strip().lower()
                if ans == "y":
                    plot_consistency_level()
            
            elif choice == "5":
                #todo: workload intensity
                print("test workload performance")

            elif choice == "6":
                simulate_node_failure(session)

            elif choice == "7":
                print("Exiting application.")
                break

            else:
                print("Invalid choice, please try again.\n")
    finally:
        if cluster:
            cluster.shutdown()
            print("Cluster connection closed.")


if __name__ == "__main__":
    main()