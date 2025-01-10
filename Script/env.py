HIBENCH_CONF_DIR = "/opt/HiBench/conf/"
HADOOP_CONF_DIR = "/opt/hadoop/etc/hadoop/"

HIBENCH_CONF_PATH = HIBENCH_CONF_DIR + "hibench.conf"
HIBENCH_REPORT_PATH = "/opt/HiBench/report/hibench.report"
SPARK_CONF_PATH = HIBENCH_CONF_DIR + "spark.conf"
MAPRED_SITE_PATH = HADOOP_CONF_DIR + "mapred-site.xml"

HIBENCH_CONF_BACKUP_PATH = HIBENCH_CONF_DIR + "hibench.conf.default"
SPARK_CONF_BACKUP_PATH = HIBENCH_CONF_DIR + "spark.conf.default"
MAPRED_SITE_BACKUP_PATH = HADOOP_CONF_DIR + "mapred-site.xml.default"

PARAMS_LOGS_PATH = "param_logs.csv"
HIBENCH_FINAL_REPORT_PATH = "hibench_final.csv"


# Parameters
n_nodes = 2
datasize = 10
n_executors = 4
executor_cores = 1
executor_memory = '640m'
driver_memory = '640m'

# 
input_split = None
parallelism = None
buffer = None
max_size_in_flight = None



