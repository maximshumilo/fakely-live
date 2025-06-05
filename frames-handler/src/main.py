from config import CONFIG
from worker.main import worker


if __name__ == '__main__':
    worker.start(workers_count=CONFIG.WORKER_COUNT)
