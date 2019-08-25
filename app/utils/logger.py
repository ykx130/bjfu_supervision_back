import logging
import logging.handlers

formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s')

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(formatter)

fileHandler = logging.handlers.TimedRotatingFileHandler(
    filename='bjfu_supervisor',
    when='midnight',
)
fileHandler.suffix = '%Y%m%d.log'
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
