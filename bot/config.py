import json

class Config(dict):
    def __init__(self, bot, *args, **kwargs):
        self.__file = "config.json"

    def load_config(self):
        __local_config = False
        try:
            with open(self.__file) as f:
                __local_config = json.load(f)
        except Exception as e:
            print (e)
        self.update(__local_config)

    def save_config(self):
        try:
            with open(__file, 'w') as f:
                json.dump(self, f, indent=2, sort_keys=True)
                # write a newline at end of file
                f.write('\n')
        except Exception as e:
            print (e)
            return False
        return True
