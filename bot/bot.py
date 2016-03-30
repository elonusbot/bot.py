from bot.config import Config

class Bot:
    def __init__(self):
        print("initializing bot")

        self.config = Config(self)
        self.restart = False

    def run(self):
        self.config.load_config()

        print (self.config)

        # while loop here?

        return self.restart
