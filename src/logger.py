import logging as lg
import os

class Logger:
    def __init__(self, logger_level=lg.INFO, streamLogs=False):
        """__init__ method for the class Logger.

        Args:
            logger_level (logging.Level, optional): Severity of logs to be recorded. Defaults to lg.INFO.
            streamLogs (bool, optional): Whether to record logss in console. Defaults to False.
        """
        # Creating a logger   
        self.logger = lg.getLogger(__name__)
        # Setting logging level to the logger
        self.logger.setLevel(logger_level)

        # Log file will go by the `name of file itself`.log
        # fetching that name of the file where the logger is to be called
        file_name = os.path.basename(os.getcwd()) + '.log'
        file_path = os.path.join('logs', file_name) # since all log files are to be saved in the logs directory.

        # Creating a File handler for the logger
        f_handler = lg.FileHandler(file_path)
        # Setting format for the file handler
        f_format = lg.formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        f_handler.setFormatter(f_format)

        # Adding file handler to the logger
        self.logger.addHandler(f_handler)

        # To return logs in the console as well
        if streamLogs:
            # Creating a handler for streaming logs
            stream_handler = lg.StreamHandler()
            # setting format to the stream handler
            stream_format = lg.formatter('%(name)s %(levelname)s %(message)s')
            stream_handler.setFormatter(stream_format)
            
            # Adding this handler to the logger
            self.logger.addHandler(stream_handler)

    def get_logger(self):
        """Returns the logger for the file where this class is called.

        Returns:
            logging.Logger: Logger for the file where this class is called.
        """
        return self.logger


