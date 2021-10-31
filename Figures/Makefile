PY_FILES = accept_models.py accept_multiprocessor_scale.py #accept_loss_rate.py
PDF_FILES = accept_models.pdf #accept_loss_rate.pdf

.PHONY: all clean

all: $(PY_FILES)
	python3.5 accept_models.py
	python3.5 accept_models_lr.py
	python3.5 accept_multiprocessor_2core.py
	python3.5 accept_multiprocessor_4core.py
	python3.5 accept_multiprocessor_8core.py
	python3.5 accept_multiprocessor_scale.py
	python3.5 second_stage.py
	python3 increasing_task.py
	python3.5 num_iterations.py
	python3.5 runtime_pipe_length.py
	python3 lbg_time.py
	python3 lbg_time_failed.py
	#python3.5 accept_loss_rate.py

clean:
	rm -rf *.pdf
