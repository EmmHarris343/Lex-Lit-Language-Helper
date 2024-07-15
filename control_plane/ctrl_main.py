from multiprocessing import Queue, Process

from .que_test_task import taskTEST     ## Where I'm running data processing

class CtrlMain:

    def __init__(self):
        print('{IPC} Initializing Ctrl Plane')

        self.que_task = taskTEST()

    def main_ctrl(self):
        print('Lets go, do the IPC thingy!!')

        input_queue = Queue()
        output_queue = Queue()
        _process = Process(target=self.que_task.doing_task, args=(input_queue, output_queue))
        _process.start()

        ## Send to process plane.
        input_queue.put(25)
        self.result_handler(output_queue.get())

        input_queue.put(13)
        self.result_handler(output_queue.get())

        input_queue.put(20)
        self.result_handler(output_queue.get())


        input_queue.put('shutdown')     ## Kill command - Process plane will not stop or close - Until ordered to shutdown

        _process.join() ## Once told to quit. This will let process close.

    def result_handler(self, result):
        print('This is what the queue did.. Sooo?', result)