from multiprocessing import Process

from .tasks import FrameHandlerTask


class Worker:

    workers: dict[int, Process] = {}

    def start(self, workers_count: int = 1) -> None:
        for worker_obj in self.workers.values():
            worker_obj.terminate()

        for _ in range(workers_count):
            worker_obj = Process(target=FrameHandlerTask.run, daemon=True)
            worker_obj.start()
            self.workers[worker_obj.pid] = worker_obj

        for worker_obj in self.workers.values():
            worker_obj.join()

    def stop(self):
        pass

worker = Worker()