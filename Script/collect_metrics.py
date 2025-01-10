import numpy as np
import pandas as pd
from prometheus_api_client import PrometheusConnect
from datetime import datetime, timedelta
from env import *

hibench_csv = pd.read_csv(HIBENCH_REPORT_PATH, delimiter=r"\s+")

hibench_csv.rename(columns={
    'Type': 'type',
    'Date': 'date',
    'Time': 'time',
    'Input_data_size': 'input_datasize_bytes',
    'Duration(s)': 'duration_s',
    'Throughput(bytes/s)': 'throughput_bytes_s',
    'Throughput/node': 'throughput_per_node_bytes_s'
}, inplace=True)




prometheus_url = "http://localhost:9090"
prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)


def get_prometheus_data(query, start_time, end_time):
    result = prom.custom_query_range(
        query=query,
        start_time=start_time,
        end_time=end_time,
        step=5
    )
    if result:
        values = [
            float(value[1]) for series in result
            for value in series["values"]
            if value[1] is not None and float(value[1]) >= 0
        ]
        return np.mean(values) if values else None
    return None


def add_prometheus_metrics_to_df(df):
    metrics = []
    for _, row in df.iterrows():
        start_time = datetime.strptime(
            f"{row['date']} {row['time']}", '%Y-%m-%d %H:%M:%S')
        end_time = start_time + timedelta(seconds=round(row['duration_s']))

        duration = round(row['duration_s'])
        cpu_query = f"""100 - (avg(rate(node_cpu_seconds_total{{mode="idle"}}[{duration}s])) * 100)"""
        ram_query = f"sum(node_memory_MemTotal_bytes - node_memory_MemFree_bytes - node_memory_Buffers_bytes - node_memory_Cached_bytes)"
  
        disk_read_query = f'rate(node_disk_read_bytes_total[{duration}s])'
        disk_write_query = f'rate(node_disk_written_bytes_total[{duration}s])'
        network_receive_query = f'rate(node_network_receive_bytes_total[{duration}s])'
        network_transmit_query = f'rate(node_network_transmit_bytes_total[{duration}s])'

        # Fetch metrics
        cpu_used = get_prometheus_data(cpu_query, start_time, end_time)
        ram_used = get_prometheus_data(ram_query, start_time, end_time)
        disk_read_speed = get_prometheus_data(
            disk_read_query, start_time, end_time)
        disk_write_speed = get_prometheus_data(
            disk_write_query, start_time, end_time)
        network_receive_speed = get_prometheus_data(
            network_receive_query, start_time, end_time)
        network_transmit_speed = get_prometheus_data(
            network_transmit_query, start_time, end_time)

        metrics.append({
            'cpu_used_percent': cpu_used,
            'ram_used_bytes': ram_used,
            'disk_read_bytes_s': disk_read_speed,
            'disk_write_bytes_s': disk_write_speed,
            'network_receive_bytes_s': network_receive_speed,
            'network_transmit_bytes_s': network_transmit_speed
        })

    df_with_metrics = pd.concat([df, pd.DataFrame(metrics)], axis=1)
    return df_with_metrics



param_logs_df = pd.read_csv(PARAMS_LOGS_PATH)
hibench_extra = add_prometheus_metrics_to_df(hibench_csv)
hibench_final = pd.concat([hibench_extra.reset_index(drop=True), param_logs_df.reset_index(drop=True)], axis=1)
hibench_final.to_csv(HIBENCH_FINAL_REPORT_PATH, index=False)

