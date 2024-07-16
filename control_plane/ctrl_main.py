from multiprocessing import Queue, Process
from colorama import init, Fore, Back, Style

## Local modules:

from .que_test_task import taskTEST     ## Where I'm running data processing

from .api_control import FlaskApp
from process_pipeline.main_pipeline import MainPipeline



class CtrlMain:

    def __init__(self):
        print('{IPC} Initializing Ctrl Plane')

        self.que_task = taskTEST()
        self.flsk_listener = FlaskApp()
        self.ProcessPipeline = MainPipeline()
        self.kill_cmd = 0

    def main_ctrl(self):
        print('Lets go, do the IPC thingy!!')




    def another_ctrl(self):
        input_queue = Queue()
        output_queue = Queue()

        cmd_queue = Queue()
        
        
        #_process = Process(target=self.que_task.doing_task, args=(input_queue, output_queue))
        #_process.start()

        #flask_process = Process(target=app.run, kwargs={'debug': False, 'use_reloader': False})
        
        ### PROCESS_KWARS EXAMPLE = Process(target=self.flsk_listener.run, kwargs={'debug': False, 'use_reloader': False})



        pipeline_proc = None # This is for a check later.

        flask_process = Process(target=self.flsk_listener.run, args=(cmd_queue,))
        flask_process.start()

        cmd_return = cmd_queue.get()
        
        print(Fore.LIGHTRED_EX + 'This was passed back from the queue (FROM API) .. ', cmd_return, Fore.RESET)

        

        json_dict_val:dict = cmd_return.get('CMD')       ## DICT get, not queue get!

        print('Keyword?', json_dict_val)

        cmd = 1
        keyword = json_dict_val

        

        cmd_val = cmd_return.get('CMD', '')
        if cmd_val != '':
            print('Yes.. Match. Start process')

            pipeline_proc = Process(target=self.ProcessPipeline._RUN, args=(cmd, keyword,))
            pipeline_proc.start()

        print('Should be back here... Am I?')
        

        if pipeline_proc:
            pipeline_proc.join()

        
        flask_process.join()            ## This doesn't close because Flask is still listening for API Calls. Have to tell flask it can close now
        #pipeline_proc.join()


        #
        #input_queue.put({'Order': 66})

        #flask_process.join()



    def result_handler(self, result):
        print('This is what the queue did.. Sooo?', result)



    def DNU_main_ctrl(self):
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

        _process.join() ## Once told to quit. This will let the main thread/ process close (this app.py)        