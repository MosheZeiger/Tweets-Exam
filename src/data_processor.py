import pandas as pd
from src.logger import Logger
from src import config
import logging
import re

logger = Logger().get_logger()

class DataProcessor:
    """
    Handles the full data processing pipeline: loading, cleaning, and preparing.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_df: pd.DataFrame | None = None
        self.processed_df: pd.DataFrame | None = None
        logger.info(f"DataProcessor initialized with file path: {self.file_path}")

    def run_processing_pipeline(self) -> pd.DataFrame | None:
        """
        Runs the full data processing pipeline in order.
        """
        logger.info("Starting data processing pipeline...")

        if self.load_csv() is None:
            logger.error("Pipeline stopped: Data loading failed.")
            return None
        initial_shape = self.processed_df.shape

        if self.select_columns(columns=config.RELEVANT_COLUMNS) is None:
            logger.error("Pipeline stopped: Column selection failed.")
            return None

        if self.remove_unclassified_rows(target_column=config.CLASSIFICATION_COLUMN) is None:
            logger.error("Pipeline stopped: Removal of unclassified rows failed.")
            return None

        if self.convert_to_lowercase(text_column=config.TEXT_COLUMN) is None:
            logger.error("Pipeline stopped: Lowercase conversion failed.")
            return None

        if self.remove_punctuation(text_column=config.TEXT_COLUMN) is None:
            logger.error("Pipeline stopped: Punctuation removal failed.")
            return None

        # More processing steps will be added here
        final_shape = self.processed_df.shape
        print(f"Initial shape: {initial_shape}, Final shape: {final_shape}")
        logger.info("--- Pipeline Summary ---")
        logger.info(f"Initial shape: {initial_shape[0]} rows, {initial_shape[1]} columns")
        logger.info(f"Final shape:   {final_shape[0]} rows, {final_shape[1]} columns")
        logger.info("------------------------")

        logger.info(f"Data processing pipeline completed. Final shape: {self.processed_df.shape}")
        return self.processed_df
    
    def load_csv(self) -> pd.DataFrame | None:
        logger.info(f"Attempting to load data from {self.file_path}")
        try:
            self.raw_df = pd.read_csv(self.file_path, encoding=config.CSV_ENCODING)
            self.raw_df.columns = self.raw_df.columns
            self.processed_df = self.raw_df.copy()
            logger.info(f"Data loaded. Initial shape: {self.processed_df.shape}")
            logger.debug(f"Data columns: {self.processed_df.columns.tolist()}")
            return self.processed_df
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return None
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None

    
    def remove_unclassified_rows(self, target_column: str) -> pd.DataFrame | None:
        if self.processed_df is None:
            logger.error("Cannot process because raw data has not been loaded.")
            return None
        if target_column not in self.processed_df.columns:
            logger.error(f"Column '{target_column}' not found in raw data.")
            return None

        initial_rows = len(self.processed_df)
        logger.info(f"Removing unclassified rows from column: {target_column}. Initial rows: {initial_rows}")
        self.processed_df = self.processed_df.dropna(subset=[target_column])
        final_rows = len(self.processed_df)
        rows_removed = initial_rows - final_rows
        
        if rows_removed > 0:
            logger.info(f"Removed {rows_removed} unclassified rows. Final shape: {self.processed_df.shape}")
        else:
            logger.info("No unclassified rows found to remove.")

        return self.processed_df


    def select_columns(self, columns: list[str]) -> pd.DataFrame | None:
        """
        Selects relevant columns from the DataFrame.
        """
        if self.processed_df is None:
            logger.error("Cannot process because raw data has not been loaded.")
            return None

        missing_cols = [col for col in columns if col not in self.processed_df.columns]
        if missing_cols:
            logger.error(f"Missing columns in the DataFrame: {missing_cols}")
            return None 
        
        logger.info(f"Selecting columns: {columns}")
        self.processed_df = self.processed_df[columns]
        logger.info(f"Columns selected. New shape: {self.processed_df.shape}")

        return self.processed_df

    def convert_to_lowercase(self, text_column: str) -> pd.DataFrame | None:
        """
        Converts the text in the specified column to lowercase.
        """
        if self.processed_df is None:
            logger.error("Cannot process because raw data has not been loaded.")
            return None
        
        if text_column not in self.processed_df.columns:
            logger.error(f"Column '{text_column}' not found in DataFrame.")
            return None

        try:
            self.processed_df[text_column] = self.processed_df[text_column].str.lower()
            logger.info(f"Converted column '{text_column}' to lowercase successfully.")
        except AttributeError as e:
            logger.error(f"Error converting to lowercase: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None
        return self.processed_df

    def remove_punctuation(self, text_column: str) -> pd.DataFrame | None:
        """
        Removes punctuation from the specified text column.
        """
        if self.processed_df is None:
            logger.error("Cannot process because raw data has not been loaded.")
            return None
        
        if text_column not in self.processed_df.columns:
            logger.error(f"Column '{text_column}' not found in DataFrame.")
            return None

        try:
            self.processed_df[text_column] = self.processed_df[text_column].apply(
                lambda x: re.sub(r'[^\w\s]', '', x) if isinstance(x, str) else x
            )
            logger.info(f"Removed punctuation from column '{text_column}' successfully.")
        except Exception as e:
            logger.error(f"An error occurred while removing punctuation: {e}")
            return None
        return self.processed_df

if __name__ == "__main__":
    logger_factory = Logger(console_level=logging.DEBUG)
    test_logger = logger_factory.get_logger()
    test_logger.info("=== Starting DataProcessor Test ===")

    
    processor = DataProcessor(file_path=config.INPUT_FILE_PATH)
    process_pipeline = processor.run_processing_pipeline()

    if process_pipeline is not None:
        test_logger.info(f"Processing pipeline completed successfully with shape: {process_pipeline.shape}")
        test_logger.info(f"Data shape after processing: {process_pipeline.shape}")
        print("\nData after pipeline run (no operations performed yet):")
        print(process_pipeline.head())
    else:
        test_logger.error("Processing pipeline failed.")
    
    test_logger.info("=== DataProcessor Test Completed ===")