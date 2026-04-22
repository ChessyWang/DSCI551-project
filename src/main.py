import sys
from setup_db import setup
from run_cl_test import run_cl_experiment
from run_failure_test import run_failure_test
from plot_results import plot_consistency_level
from write_client import insert_sample_data
from cassandra_client import create_session
from query_client import query_recent
from read_after_write_test import run_consistency_demo
from benchmark_schema import test_run_schema_exploration
from benchmark import test_run_intensity_experiment

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
    try:
        user_input = input("Enter number of rounds (default 5): ").strip()

        if user_input == "":
            rounds = 5
        else:
            rounds = int(user_input)

        # 防止太离谱
        if rounds <= 0:
            print("Invalid input, using default = 5")
            rounds = 5
        elif rounds > 10000:
            print("Too large, capping at 100 for demo")
            rounds = 3000

    except ValueError:
        print("Invalid input, using default = 5")
        rounds = 5

    # run_cl_experiment(session)
    run_consistency_demo(session, rounds)

    print("\nConsistency comparison finished.\n")

def schema_test(session = None):
    test_run_schema_exploration(session)
    return

def simulate_workload_intensity(session=None):
    print("\n=== Workload Intensity Simulation ===")
    print("Simulating increasing workload intensity and observing system behavior...\n")

    test_run_intensity_experiment(session)
    print("\nWorkload intensity simulation finished.\n")

    return

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
    print("1. Ingest sensor data") # 5000
    print("2. View latest sensor readings") # device_id
    print("3. Analyze partition key impact") # 
    print("4. Check recent data consistency") # read after write stale read
    print("5. Simulate high traffic workload") # 
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
                schema_test(session)
            
            elif choice == "4":
                compare_consistency_modes(session)
                # ans = input("Plot results now? (y/n): ").strip().lower()
                # if ans == "y":
                #     plot_consistency_level()
            
            elif choice == "5":
                simulate_workload_intensity(session)

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