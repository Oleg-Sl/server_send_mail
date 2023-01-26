from threading import Thread, Lock

from . import send_email


class ArrThreads:
    def __init__(self, input_queue, count_threads=1):
        self.input_queue = input_queue
        self.count_threads = count_threads
        self.threads = []

    def send_queue_stop_threads(self):
        [self.input_queue.put(None) for _ in range(self.count_threads)]

    def create(self):
        if not self.threads:
            self.threads = [Thread(target=self.handler) for _ in range(self.count_threads)]

    def start(self):
        [thread.start() for thread in self.threads]

    def join(self):
        [thread.join() for thread in self.threads]

    def handler(self):
        pass


class ThreadsSendEmail(ArrThreads):
    def __init__(self, input_queue, count_threads):
        super().__init__(input_queue, count_threads)

    def handler(self):
        while True:
            data = self.input_queue.pop()
            if not isinstance(data, dict):
                break
            send_email.send(data)
            self.input_queue.task_done()
