import pandas as pd
import os
from datetime import datetime
from env import *

params = {
    "num_nodes" : n_nodes,
    "num_executors": n_executors,
    "executor_cores": executor_cores,
    "executor_memory_mb": executor_memory,
    "input_split_mb": input_split,
    "buffer_kb": buffer,
    "max_size_in_flight_mb": max_size_in_flight,
    "parallelism": parallelism,
}

def track_params(params=params, file_path=PARAMS_LOGS_PATH):
    current_time = datetime.now()
    date = current_time.strftime('%Y-%m-%d')  
    time = current_time.strftime('%H:%M:%S') 
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=list(params.keys()) + ['date','time'])

        params['date'] = date
        params['time'] = time
        new_entry = pd.DataFrame([params])
        df = pd.concat([df, new_entry], ignore_index=True)

        df.to_csv(file_path, index=False)
        print(f"Đã lưu params vào {file_path}")
    except Exception as e:
        print(f"Lỗi khi lưu params: {e}")

if __name__ == "__main__":
    track_params()