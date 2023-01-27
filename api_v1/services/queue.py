from queue import Queue


# Очередь писем на отправку
class EmailsQueue:
    def __init__(self, count_threads):
        self.input_queue = Queue()
        self.count_threads = count_threads
        self.max_size = None

    def send_queue(self, item):
        self.input_queue.put(item)

    def pop(self):
        return self.input_queue.get()

    def task_done(self):
        self.input_queue.task_done()

    def send_queue_stop(self):
        [self.send_queue(None) for _ in range(self.count_threads)]

    def qsize(self):
        return self.input_queue.qsize()

    def set_start_size(self, size_q):
        self.max_size = size_q

    def get_start_size(self):
        return self.max_size

