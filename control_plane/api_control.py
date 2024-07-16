# control_plane/api_control.py

from colorama import init, Fore, Back, Style
from multiprocessing import Queue

import requests
from flask import Flask, request, jsonify

## Test CURL: curl -i -X POST -H "Content-Type: application/json" -d "{\"Test\":\"Potatos!\"}" http://localhost:5000/api/listen

class FlaskApp:
    

    def __init__(self):
        self.app = Flask(__name__)
        self.command_queue = Queue
        #self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/api/listen', methods=['POST'])
        def listening():
            data = request.json
            print(Fore.LIGHTCYAN_EX + "Received data from frontend:", data, Fore.RESET)
            # Do tasks here?
            
            self.command_queue.put(data)

            
            
            #APICtrl.main(self)

            # Returns message to API call: 
            re_res = {'message': 'Did task in back-end'}
            return jsonify(re_res), 200

    def run(self, queue_con: Queue):
        self.setup_routes()
        self.command_queue = queue_con
        
        # 'debug': False, 'use_reloader': False
        self.app.run(debug=True, use_reloader = False)

    def data_que(self, input_queue, output_queue):
        pass




class APICtrl:
    def __init__(self):
        pass
    def main(self):
        print('Api CTRL eh')


if __name__ == '__main__':
    flask_app = FlaskApp()
    flask_app.run()