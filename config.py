import os
import multiprocessing

config = {
    'PROCESS_POOL_SIZE': multiprocessing.cpu_count(),
    'TENSORFLOW_MODEL_PATH': '/tf',
    'PORT': 80
}

for k, v in config.items():
    config[k] = os.getenv(k, v)
