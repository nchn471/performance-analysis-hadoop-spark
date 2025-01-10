start_hadoop:
	sudo -u hadoop bash -c "/opt/hadoop/sbin/start-dfs.sh && \
	/opt/hadoop/sbin/start-yarn.sh && \
	/opt/spark/sbin/start-history-server.sh && /opt/hadoop/bin/hdfs dfsadmin -safemode leave && jps"

stop_hadoop:
	sudo -u hadoop bash -c "/opt/hadoop/sbin/stop-dfs.sh && \
	/opt/hadoop/sbin/stop-yarn.sh && \
	/opt/spark/sbin/stop-history-server.sh && jps"

restart_hadoop:
	make stop_hadoop && make start_hadoop

tuning:
	sudo .venv/bin/python tuning.py

prepare_wordcount:
	make tuning
	sudo -u hadoop bash -c ". /opt/python/hibench_env/bin/activate && /opt/HiBench/bin/workloads/micro/wordcount/prepare/prepare.sh"
	echo -e "\a"

prepare_terasort:
	make tuning
	sudo -u hadoop bash -c ". /opt/python/hibench_env/bin/activate && /opt/HiBench/bin/workloads/micro/terasort/prepare/prepare.sh"
	echo -e "\a"

run_wordcount:
	make tuning
	sudo -u hadoop bash -c ". /opt/python/hibench_env/bin/activate && /opt/HiBench/bin/workloads/micro/wordcount/spark/run.sh"
	python track_params.py 
	echo -e "\a"


run_terasort:
	make tuning
	sudo -u hadoop bash -c ". /opt/python/hibench_env/bin/activate && /opt/HiBench/bin/workloads/micro/terasort/spark/run.sh"
	.venv/bin/python track_params.py
	echo -e "\a"


make clear_report:
	sudo rm /opt/HiBench/report/hibench.report

collect_metrics:																																													 																	
	sudo .venv/bin/python collect_metrics.py

auto_wordcount:

	for input_split_value in 128 256 512 1024; do \
		.venv/bin/python change_params.py --input_split $$input_split_value; \
		make run_wordcount; \
	done

	for parallelism_value in 4 8 10 12; do \
        .venv/bin/python change_params.py --parallelism $$parallelism_value; \
		make run_wordcount; \
	done

auto_terasort:

	for input_split_value in 128 256 512 1024; do \
		.venv/bin/python change_params.py --input_split $$input_split_value; \
		make run_terasort; \
	done

	for pair in "16k 32m" "32k 48m" "48k 64m" "64k 96m"; do \
		set -- $$pair; \
		.venv/bin/python change_params.py --buffer $$1 --max_size_in_flight $$2; \
		make run_terasort; \
	done
	make collect_metrics
	sudo shutdown




																					 