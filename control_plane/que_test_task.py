from multiprocessing import Queue

class taskTEST:
    def __init__(self):
        pass

    def main(self):
        print('QUE TASK test ---')

    ## Adding :Queue might break it.. sooo maybe remove that
    def doing_task(self, input_queue: Queue, output_queue: Queue) -> None:
        while True:
            data_from_queue = input_queue.get()

            print('Data Incoming.. Processing', data_from_queue)
            math_final = 0

            if type(data_from_queue) is int:                
                if data_from_queue == int(25):
                    print(' - Match its 25')
                    math_data = data_from_queue
                    math_value = 20+30
                    combine_math = math_data + math_value

                    # should be what.. 47 +/- whatever is passed.
                    math_final = combine_math -3

                elif data_from_queue == int(20):
                    print(' - Match its 20')
                    math_data = data_from_queue
                    math_value = 20+30
                    combine_math = math_data + math_value

                    # should be what.. 47 +/- whatever is passed.
                    math_final = combine_math -3

                elif data_from_queue == int(30):
                    print(' - Match its 30')
                    math_data = data_from_queue
                    math_value = 20+30
                    combine_math = math_data + math_value

                    # should be what.. 47 +/- whatever is passed.
                    math_final = combine_math -3

                else:
                    math_final = '! No-Match !'


                output_queue.put(math_final)
            if type(data_from_queue) is str and data_from_queue == 'shutdown':
                break