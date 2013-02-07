import logging
import logging.handlers


def create_logger(logName, logLevel='debug', logFile='test.log', stream=0):
    LOG_FILENAME = logFile
    # Files will rotate at 200MB
    MAX_BYTES = 209715200
    # Files versions to keep
    BACKUP_COUNT = 10
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
    logLevel = LEVELS.get(logLevel, logging.NOTSET)

    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger(logName)
    my_logger.setLevel(logLevel)
    if(logFile != 0 and logFile != ''):
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to ch
        handler.setFormatter(formatter)
        my_logger.addHandler(handler)
    # If required we print out stream, or if no logFile was specified
    if(stream != 0 or logFile == 0 or logFile == ''):
            handler = logging.StreamHandler()
            my_logger.addHandler(handler)
    return my_logger
