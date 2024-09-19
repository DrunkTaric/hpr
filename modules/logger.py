import logging
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('settings.json')

logging.basicConfig(level=logging.DEBUG)

class log:
    def __init__(self, name):
        self.path = f'Logs/{name}.log'
        self.logger = logging.getLogger(name)
        self.handler = logging.FileHandler(self.path)
        self.formatter = logging.Formatter('%(asctime)s - [%(levelname)s] => %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        
    def Color(self, r, g, b, txt):
        return f"\033[38;2;{r};{g};{b}m{txt}\033[38;2;255;255;255m"
        
    def write(self, type, message):
        if type == "info" and config.logger.info: self.logger.info(message)
        if type == "error" and config.logger.error: self.logger.error(message)
        if type == "warning" and config.logger.warning: self.logger.warning(message)
        if type == "debug" and config.logger.debug: self.logger.debug(message)