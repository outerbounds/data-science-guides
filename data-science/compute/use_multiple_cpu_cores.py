from metaflow import FlowSpec, step, Parameter
from concurrent import futures
import time

def do_task(name):
    time.sleep(3) # a long-running task
    return name

class MulticoreFlow(FlowSpec):

    #highlight-next-line
    num_cores = Parameter('num-cores', default=4)

    @step
    def start(self):
        threads = [
            "thread_%s" % i 
            for i in range(self.num_cores)
        ]
        t0 = time.time()
        #highlight-start
        with futures.ThreadPoolExecutor(
            max_workers = self.num_cores
        ) as exe:
            self.messages = [
                msg for msg in exe.map(do_task, threads)
            ]
        #highlight-end
        self.time_elapsed = time.time() - t0
        self.next(self.end)

    @step
    def end(self):
        print_msg = "All tasks completed in %.3fs"
        print(print_msg % self.time_elapsed)
        [print(msg) for msg in self.messages]

if __name__ == '__main__':
    MulticoreFlow()
