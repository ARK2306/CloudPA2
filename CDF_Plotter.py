import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_cdf_and_calculate_percentiles(file_path):
    # Read the latency results from the CSV file
    df = pd.read_csv(file_path)

    # Extract latency values
    latencies = df['Latency (seconds)'].values

    # Sort the latency values
    sorted_latencies = np.sort(latencies)

    # Calculate the CDF
    cdf = np.arange(1, len(sorted_latencies) + 1) / len(sorted_latencies)

    # Calculate the 90th and 95th percentiles
    p90 = np.percentile(latencies, 90)
    p95 = np.percentile(latencies, 95)

    # Print the percentile values
    print(f"90th Percentile Latency: {p90:.4f} seconds")
    print(f"95th Percentile Latency: {p95:.4f} seconds")

    # Plotting the CDF
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_latencies, cdf, marker='.', linestyle='none')
    plt.title('Cumulative Distribution Function (CDF) of Latency')
    plt.xlabel('Latency (seconds)')
    plt.ylabel('CDF')
    plt.grid(True)
    plt.xlim(0, sorted_latencies[-1])  # Limit x-axis to the max latency
    plt.ylim(0, 1)  # Y-axis from 0 to 1
    plt.axhline(y=0.9, color='g', linestyle='--', label='90th Percentile')  # 90th percentile line
    plt.axvline(x=p90, color='g', linestyle='--')  # 90th percentile value line
    plt.axhline(y=0.95, color='b', linestyle='--', label='95th Percentile')  # 95th percentile line
    plt.axvline(x=p95, color='b', linestyle='--')  # 95th percentile value line
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Specify the path to your latency results CSV file
    file_path = '/Users/aryanreddy/Desktop/latency_results_producer_4.csv'  # Adjust as needed
    plot_cdf_and_calculate_percentiles(file_path)
