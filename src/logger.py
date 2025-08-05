import logging
import datetime
import os
from pathlib import Path

class Logger:
    """
    A configurable Singleton Logger class.
    
    Ensures a single logging instance across the application with configurable
    levels for the main logger, file output, and console output.
    
    Usage:
        logger = Logger().get_logger()
        logger.info("This is an info message.")
    """
    _instance = None
    _initialized = False
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self,
                 name: str = 'logger',
                 logs_dir: str = 'logs',
                 main_level: int = logging.INFO,
                 file_level: int = logging.INFO,
                 console_level: int = logging.ERROR):
        """
        Initializes the Logger singleton.
        
        Args:
            name (str): The name of the logger.
            logs_dir (str): The directory to save log files in.
            main_level (int): The main gatekeeper level. Messages below this level
                              will be ignored entirely. Must be <= the handler levels
                              for them to be effective.
            file_level (int): The logging level for the file handler.
            console_level (int): The logging level for the console handler.
        """
        if self._initialized:
            return
        
        try:
            # Assumes the script is in a subdirectory of the project root (e.g., /src)
            project_root = Path(__file__).resolve().parent.parent
        except NameError:
            project_root = Path().cwd()  # Fallback to current working directory
        except Exception as e:
            print(f"Error determining project root: {e}")
            project_root = Path().cwd().resolve()  # Fallback to current working directory

        self.logs_dir = project_root / logs_dir
        self.main_level = main_level
        self.file_level =  file_level
        self.console_level = console_level

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.main_level)

        self._setup_handlers()
        Logger._initialized = True

    def _setup_handlers(self):
        """Private method to set up file and console handlers."""
        os.makedirs(self.logs_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')
        log_filename = os.path.join(self.logs_dir, f'log_{timestamp}.log')

        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
                )
            

            file_handler = logging.FileHandler(log_filename, mode='w')
            file_handler.setLevel(self.file_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.console_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger


