import sys
from run_cl_test import run_cl_experiment
from run_failure_test import run_failure_test

def simulate_device_ingestion():
    print("\n=== Data Ingestion ===")
    print("Simulating devices sending sensor data to Cassandra...\n")

    # todo: insert data
    # e.g. insert_data()
    print("Data ingestion completed.\n")


def query_recent_readings():
    print("\n=== Query Recent Data ===")
    print("Fetching latest sensor readings...\n")

    # todo: query data
    # e.g. query_data()
    print("Query completed.\n")


def compare_consistency_modes():
    print("\n=== Consistency Mode Comparison ===")
    print("Comparing performance under different consistency levels (ONE vs QUORUM)...\n")

    run_cl_experiment()

    print("\nConsistency comparison finished.\n")


def simulate_node_failure():
    print("\n=== Node Failure Simulation ===")
    print("Simulating failure of one Cassandra node and observing system behavior...\n")

    run_failure_test()

    print("\nFailure simulation finished.\n")

#Todo: schema + workload test


def print_menu():
    print("\n==============================")
    print(" Distributed IoT Data Platform ")
    print("==============================")
    print("1. Ingest sensor data")
    print("2. Query recent readings")
    print("3. Compare consistency modes")
    print("4. Simulate node failure")
    print("5. Analyze partition key impact")
    print("6. Performance Under Load")
    print("7. Exit")
    print("==============================")


def main():
    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            simulate_device_ingestion()

        elif choice == "2":
            query_recent_readings()

        elif choice == "3":
            compare_consistency_modes()

        elif choice == "4":
            simulate_node_failure()
        
        elif choice == "5":
            #todo: schema test
            print("test schema")

        elif choice == "6":
            #todo: workload intensity
            print("test workload performance")

        elif choice == "7":
            print("Exiting application.")
            sys.exit(0)

        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main()