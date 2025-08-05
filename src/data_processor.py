import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent

import pandas as pd
from src.logger import Logger
from src import config
import logging


logger = Logger().get_logger()

class DataProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_df: pd.DataFrame | None = None
        logger.info(f"DataProcessor initialized with file path: {self.file_path}")

    def load_csv(self) -> pd.DataFrame | None:
        logger.info(f"Attempting to load data from {self.file_path}")
        try:
            self.raw_df = pd.read_csv(self.file_path, encoding=config.CSV_ENCODING)
            logger.info(f"Data loaded successfully with shape: {self.raw_df.shape}")
            logger.debug(f"Data columns: {self.raw_df.columns.tolist()}")
            return self.raw_df
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return None
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None


if __name__ == "__main__":
    logger_factory = Logger(console_level=logging.DEBUG)
    test_logger = logger_factory.get_logger()
    test_logger.info("=== Starting DataProcessor Test ===")

    input_file = config.DATA_DIR / 'tweets_dataset.csv'
    processor_for_testing = DataProcessor(file_path=input_file)
    df = processor_for_testing.load_csv()
    if df is not None:
        test_logger.info(f"DataFrame loaded with {df.shape[0]} rows and {df.shape[1]} columns.")
        print("\nFirst 5 rows of the loaded dataframe:")
        print(df.head())
    else:
        test_logger.error("Failed to load DataFrame.")
    test_logger.info("--- DataProcessor test completed ---")

