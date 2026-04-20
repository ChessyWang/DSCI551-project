import pandas as pd
import matplotlib.pyplot as plt


CSV_FILE = "schema_results.csv"


def plot_throughput_by_schema(df):
    grouped = df.groupby("schema_name", as_index=False)["throughput_ops_sec"].mean()

    plt.figure(figsize=(8, 5))
    plt.bar(grouped["schema_name"], grouped["throughput_ops_sec"])
    plt.xlabel("Schema")
    plt.ylabel("Average Throughput (ops/sec)")
    plt.title("Average Throughput by Schema")
    plt.xticks(rotation=15)
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig("schema_throughput.png")
    plt.show()


def plot_avg_latency_by_schema(df):
    grouped = df.groupby("schema_name", as_index=False)["avg_latency_ms"].mean()

    plt.figure(figsize=(8, 5))
    plt.bar(grouped["schema_name"], grouped["avg_latency_ms"])
    plt.xlabel("Schema")
    plt.ylabel("Average Latency (ms)")
    plt.title("Average Latency by Schema")
    plt.xticks(rotation=15)
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig("schema_avg_latency.png")
    plt.show()


def plot_p95_latency_by_schema(df):
    grouped = df.groupby("schema_name", as_index=False)["p95_latency_ms"].mean()

    plt.figure(figsize=(8, 5))
    plt.bar(grouped["schema_name"], grouped["p95_latency_ms"])
    plt.xlabel("Schema")
    plt.ylabel("P95 Latency (ms)")
    plt.title("P95 Latency by Schema")
    plt.xticks(rotation=15)
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig("schema_p95_latency.png")
    plt.show()


def plot_throughput_vs_concurrency(df):
    schemas = df["schema_name"].unique()

    plt.figure(figsize=(8, 5))
    for schema in schemas:
        sub = df[df["schema_name"] == schema].sort_values("concurrency")
        plt.plot(sub["concurrency"], sub["throughput_ops_sec"], marker="o", label=schema)

    plt.xlabel("Concurrency")
    plt.ylabel("Throughput (ops/sec)")
    plt.title("Throughput vs Concurrency by Schema")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("throughput_vs_concurrency.png")
    plt.show()


def plot_latency_vs_concurrency(df):
    schemas = df["schema_name"].unique()

    plt.figure(figsize=(8, 5))
    for schema in schemas:
        sub = df[df["schema_name"] == schema].sort_values("concurrency")
        plt.plot(sub["concurrency"], sub["avg_latency_ms"], marker="o", label=schema)

    plt.xlabel("Concurrency")
    plt.ylabel("Average Latency (ms)")
    plt.title("Average Latency vs Concurrency by Schema")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("latency_vs_concurrency.png")
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv(CSV_FILE)
    print(df)

    plot_throughput_by_schema(df)
    plot_avg_latency_by_schema(df)
    plot_p95_latency_by_schema(df)
    plot_throughput_vs_concurrency(df)
    plot_latency_vs_concurrency(df)