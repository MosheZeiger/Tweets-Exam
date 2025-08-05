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

    def remove_unclassified_rows(self, target_column: str) -> pd.DataFrame | None:
        if self.raw_df is None:
            logger.error("Cannot process because raw data has not been loaded.")
            return None
        if target_column not in self.raw_df.columns:
            logger.error(f"Column '{target_column}' not found in raw data.")
            return None

        initial_rows = len(self.raw_df)
        logger.info(f"Removing unclassified rows from column: {target_column}. Initial rows: {initial_rows}")
        self.cleaned_df = self.raw_df.dropna(subset=[target_column])
        final_rows = len(self.cleaned_df)
        rows_removed = initial_rows - final_rows
        logger.info(f"Finished removal. Removed {rows_removed} rows. Final rows: {final_rows}")

        try:
            self.cleaned_df = self.cleaned_df.astype({target_column: int})
            logger.debug(f"Converted column '{target_column}' to integer type.")
        except (ValueError, TypeError) as e:
            logger.warning(f"Could not convert column '{target_column}' to integer: It might contain non-numeric values. Error: {e}")
        return self.cleaned_df



if __name__ == "__main__":
    logger_factory = Logger(console_level=logging.DEBUG)
    test_logger = logger_factory.get_logger()
    test_logger.info("=== Starting DataProcessor Test ===")

    input_file = config.DATA_DIR / 'tweets_dataset.csv'
    processor_for_testing = DataProcessor(file_path=input_file)
    

    # # test loading CSV
    # df = processor_for_testing.load_csv()
    # if df is not None:
    #     test_logger.info(f"DataFrame loaded with {df.shape[0]} rows and {df.shape[1]} columns.")
    #     print("\nFirst 5 rows of the loaded dataframe:")
    #     print(df.head())
    # else:
    #     test_logger.error("Failed to load DataFrame.")
    # test_logger.info("--- DataProcessor test completed ---")

    # test removing unclassified rows
    df_raw = processor_for_testing.load_csv()
    if df_raw is None:
        test_logger.error("Failed to load DataFrame. aborting test.")
    else:
        test_logger.info(f"Raw DataFrame loaded with {df_raw.shape[0]} rows and {df_raw.shape[1]} columns.")
        test_logger.info("\nTesting Removing unclassified rows method ---")
        from src.config import CLASSIFICATION_COLUMN 
        df_cleaned = processor_for_testing.remove_unclassified_rows(target_column=CLASSIFICATION_COLUMN)
        if df_cleaned is not None:
            test_logger.info(f"Cleaned DataFrame has {df_cleaned.shape[0]} rows")
            test_logger.info(f"Types of '{CLASSIFICATION_COLUMN}' column: {df_cleaned[CLASSIFICATION_COLUMN].dtype}")
            print("\nFirst 5 rows of the cleaned dataframe:")
            print(df_cleaned.head())
        else:
            test_logger.error("Failed to clean DataFrame.")
    test_logger.info("--- DataProcessor test completed ---")

