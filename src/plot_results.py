import pandas as pd
import matplotlib.pyplot as plt


def plot_workload_intensity(df: pd.DataFrame):
    sub = df[df["experiment_type"] == "workload_intensity"].copy()
    if sub.empty:
        print("No workload_intensity data found.")
        return

    sub = sub.sort_values("concurrency")

    plt.figure(figsize=(8, 5))
    plt.plot(sub["concurrency"], sub["throughput_ops_sec"], marker="o")
    plt.xlabel("Concurrency")
    plt.ylabel("Throughput (ops/sec)")
    plt.title("Workload Intensity vs Throughput")
    plt.grid(True)
    plt.savefig("workload_throughput.png")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(sub["concurrency"], sub["avg_latency_ms"], marker="o")
    plt.xlabel("Concurrency")
    plt.ylabel("Average Latency (ms)")
    plt.title("Workload Intensity vs Average Latency")
    plt.grid(True)
    plt.savefig("workload_avg_latency.png")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(sub["concurrency"], sub["p95_latency_ms"], marker="o")
    plt.xlabel("Concurrency")
    plt.ylabel("P95 Latency (ms)")
    plt.title("Workload Intensity vs P95 Latency")
    plt.grid(True)
    plt.savefig("workload_p95_latency.png")
    plt.show()


def plot_read_write_mix(df: pd.DataFrame):
    sub = df[df["experiment_type"] == "read_write_mix"].copy()
    if sub.empty:
        print("No read_write_mix data found.")
        return

    x = sub["workload_name"]

    plt.figure(figsize=(8, 5))
    plt.bar(x, sub["throughput_ops_sec"])
    plt.xlabel("Workload")
    plt.ylabel("Throughput (ops/sec)")
    plt.title("Read/Write Mix vs Throughput")
    plt.grid(True, axis="y")
    plt.savefig("mix_throughput.png")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.bar(x, sub["avg_latency_ms"])
    plt.xlabel("Workload")
    plt.ylabel("Average Latency (ms)")
    plt.title("Read/Write Mix vs Average Latency")
    plt.grid(True, axis="y")
    plt.savefig("mix_avg_latency.png")
    plt.show()


def plot_replication_factor(df: pd.DataFrame):
    sub = df[df["experiment_type"] == "replication_factor"].copy()
    if sub.empty:
        print("No replication_factor data found.")
        return

    sub = sub.sort_values("replication_factor")

    plt.figure(figsize=(8, 5))
    plt.plot(sub["replication_factor"], sub["throughput_ops_sec"], marker="o")
    plt.xlabel("Replication Factor")
    plt.ylabel("Throughput (ops/sec)")
    plt.title("Replication Factor vs Throughput")
    plt.grid(True)
    plt.savefig("rf_throughput.png")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(sub["replication_factor"], sub["avg_latency_ms"], marker="o")
    plt.xlabel("Replication Factor")
    plt.ylabel("Average Latency (ms)")
    plt.title("Replication Factor vs Average Latency")
    plt.grid(True)
    plt.savefig("rf_avg_latency.png")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(sub["replication_factor"], sub["p95_latency_ms"], marker="o")
    plt.xlabel("Replication Factor")
    plt.ylabel("P95 Latency (ms)")
    plt.title("Replication Factor vs P95 Latency")
    plt.grid(True)
    plt.savefig("rf_p95_latency.png")
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv("results.csv")
    print(df)

    plot_workload_intensity(df)
    plot_read_write_mix(df)
    plot_replication_factor(df)