import json


from app_conf import Configuration

class write_json:

    def __init__(self):
        conf = Configuration
        self.conf = conf
        

    def save_to_output(self, data_tosave: list[dict]) -> None:
        print(':: FUNCTION :: Save to Json')
        try:
            with open(self.conf.json_output_file, 'w') as f:
                json.dump(data_tosave, f, indent=4)
        except Exception as err:
            self.excption_handling(0, err, "Failure when trying to save output data to json file!")



class read_json:

    def read_json_data(self, data_tosave: list[dict]) -> None:
        print('Read Process data from Json file(s)')