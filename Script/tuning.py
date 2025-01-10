import re
import os
import shutil
import pandas as pd
from env import *


def convert_to_bytes(unit, type="g"):
    if not unit:
        return None
    if type == "g":
        return int(unit * 1024**3)
    elif type == "m":
        return int(unit * 1024**2)
    else:
        raise ValueError(
            "Type must be either 'g' for gigabytes or 'm' for megabytes.")


datasize_params = {
    "hibench.datasize": convert_to_bytes(datasize)
}
# spark.conf
spark_conf_params = {
    "hibench.yarn.executor.num": n_executors,
    "hibench.yarn.executor.cores": executor_cores,
    "spark.executor.memory": executor_memory,
    "spark.driver.memory" : driver_memory
}
wordcount_params = {
    "spark.default.parallelism": parallelism,
    "spark.sql.shuffle.partitions": parallelism
}
terasort_params = {
    "spark.shuffle.file.buffer": buffer,
    "spark.reducer.maxSizeInFlight": max_size_in_flight,
}
# mapred-site.xml
mapred_site_params = {
    "mapreduce.input.fileinputformat.split.minsize": convert_to_bytes(input_split, type = "m")
}

def reset_default_config():

    config_files = [
        (HIBENCH_CONF_BACKUP_PATH, HIBENCH_CONF_PATH),
        (SPARK_CONF_BACKUP_PATH, SPARK_CONF_PATH),
        (MAPRED_SITE_BACKUP_PATH, MAPRED_SITE_PATH),
    ]

    for backup_path, target_path in config_files:
        try:
            if os.path.exists(backup_path):
                shutil.copy(backup_path, target_path)
                print(f"Đã reset {target_path}")
            else:
                print(f"Không tìm thấy file backup: {backup_path}. Bỏ qua...")
        except Exception as e:
            print(f"Không thể reset {target_path}: {e}")


def modify_conf(file_path, updates):

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            updated = False
            for key, new_value in updates.items():
                if key in line and not line.strip().startswith("#"):
                    line = re.sub(
                        rf"({key}\s+).*", lambda m: f"{m.group(1)}{new_value}", line)
                    updated = True
                    print(f"Đã cập nhật: {line.strip()}")
                    break
            file.write(line)

        for key, new_value in updates.items():
            key_found = any(key in line for line in lines)
            if not key_found:
                file.write(f"{key} {new_value}\n")
                print(f"Đã thêm: {key}\t{new_value}")


def modify_xml(file_path, updates):
    try:
        with open(file_path, 'r+') as file:
            content = file.read()

            for key, new_value in updates.items():
                pattern = rf"(<property>\s*<name>{re.escape(key)}</name>\s*<value>)(\d+)(</value>\s*</property>)"

                if re.search(pattern, content):
                    content = re.sub(pattern, lambda m: f"{m.group(1)}{new_value}{m.group(3)}", content)
                    print(f"Đã sửa key '{key}' thành '{new_value}' trong file {file_path}")
                else:
                    new_property = f"    <property>\n        <name>{key}</name>\n        <value>{new_value}</value>\n    </property>\n\n"
                    if "</configuration>" in content:
                        content = content.replace(
                            "</configuration>", new_property + "</configuration>")
                        print(f"Đã thêm key '{key}' với giá trị '{new_value}' trong file {file_path}")
                    else:
                        print(
                            f"Lỗi: Không tìm thấy thẻ đóng </configuration> trong file {file_path}")

            file.seek(0)
            file.write(content)
            file.truncate()

    except Exception as e:
        print(f"Không thể sửa file {file_path}: {e}")


if __name__ == "__main__":

    reset_default_config()
    # hibench.conf

    # dataset size
    modify_conf(HIBENCH_CONF_PATH, datasize_params)
    # resource
    modify_conf(SPARK_CONF_PATH, spark_conf_params)
    # input split
    if input_split: 
        modify_xml(MAPRED_SITE_PATH,mapred_site_params)
    # shuffle
    if parallelism:
        modify_conf(SPARK_CONF_PATH,wordcount_params)
    if buffer and max_size_in_flight:
        modify_conf(SPARK_CONF_PATH, terasort_params)
