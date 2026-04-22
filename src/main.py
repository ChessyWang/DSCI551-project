import sys
from db.setup_db import setup
from db.cassandra_client import create_session

from utils.plot_results import plot_consistency_level
from write_client import insert_sample_data

from query_client import query_recent
from benchmark.benchmark_schema import test_run_schema_exploration
from benchmark.benchmark import test_run_intensity_experiment

from experiments import (
    run_cl_experiment,
    run_failure_test,
    run_consistency_demo,
)

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

def print_consistency_menu():
    print("\n--- Consistency Analysis ---")
    print("1. Check recent data consistency")
    print("2. Compare consistency levels (plot)")
    print("3. Back to main menu")

def consistency_analysis(session = None):
    print("Comparing performance under different consistency levels (ONE vs QUORUM)...\n")
    while True:
        print_consistency_menu()
        sub_choice = input("Select an option: ").strip()
        if sub_choice == "1":
            try:
                user_input = input("Enter number of rounds (default 5): ").strip()

                if user_input == "":
                    rounds = 5
                else:
                    rounds = int(user_input)
                if rounds <= 0:
                    print("Invalid input, using default = 5")
                    rounds = 5
                elif rounds > 10000:
                    print("Too large, capping at 3000 for demo")
                    rounds = 3000

            except ValueError:
                print("Invalid input, using default = 5")
                rounds = 5

            run_consistency_demo(session, rounds)
        elif sub_choice == "2":
            run_cl_experiment(session)
            ans = input("Plot results now? (y/n): ").strip().lower()
            if ans == "y":
                plot_consistency_level()

        elif sub_choice == "3":
            break
        else:
                print("Invalid choice, try again.")

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


def print_main_menu():
    print("\n==============================")
    print(" Distributed IoT Data Platform ")
    print("==============================")
    print("1. Ingest sensor data") # 5000
    print("2. View latest sensor readings") # device_id
    print("3. Analyze partition key impact") # 
    print("4. Sensor Data Consistency Analysis") # read after write stale read
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
            print_main_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                simulate_device_ingestion(session)

            elif choice == "2":
                query_recent_readings(session)
            
            elif choice == "3":
                schema_test(session)
            
            elif choice == "4":
                consistency_analysis(session)
            
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