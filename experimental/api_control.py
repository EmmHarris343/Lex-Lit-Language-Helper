# experimental/api_control.py


import requests
from flask import Flask, request, jsonify



## Test CURL: curl -i -X POST -H "Content-Type: application/json" -d "{\"Test\":\"Potatos!\"}" http://localhost:5000/api/listen


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/api/listen', methods=['POST'])
        def listening():
            data = request.json
            print("Received data from frontend:", data)
            # Do tasks here?
            
            APICtrl.main(self)

            # Returns message to API call: 
            re_res = {'message': 'Did task in back-end'}
            return jsonify(re_res), 200
        
    def run(self):
        self.app.run(debug=True)



class APICtrl:

    def __init__(self):
        pass

    def main(self):
        print('Api CTRL eh')


if __name__ == '__main__':
    flask_app = FlaskApp()
    flask_app.run()