import pandas as pd
import json
from src.logger import Logger
from src import config
from pathlib import Path
import logging

# Import the formatters
from src.formatters import BaseFormatter

logger = Logger().get_logger()

class ReportGenerator:
    """
    A generic report generator. Can use a provided formatter to shape the JSON output.
    """
    def __init__(self, exploration_results: dict, cleaned_df: pd.DataFrame, formatter: BaseFormatter = BaseFormatter()):
        """
        Initializes the ReportGenerator.

        Args:
            exploration_results (dict): The dictionary of analysis results.
            cleaned_df (pd.DataFrame): The cleaned pandas DataFrame.
            formatter (BaseFormatter): An optional formatter object to shape the JSON output.
        """
        self.raw_results = exploration_results
        self.df = cleaned_df
        self.formatter = formatter
        self.results_dir = Path(config.RESULTS_DIR)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"ReportGenerator initialized with formatter: {type(formatter).__name__}")

    def generate_all_reports(self) -> None:
        """
        Generates all reports: CSV and JSON.
        """
        logger.info("Starting report generation...")
        self.generate_csv_report()
        self.generate_json_report()
        logger.info("Report generation completed.")

    def generate_csv_report(self, output_path: str = config.CLEANED_CSV_PATH) -> None:
        """
        Generates a CSV report of the cleaned DataFrame.
        """
        logger.info(f"Generating CSV report at {output_path}")
        try:
            self.df.to_csv(output_path, index=False, encoding='utf-8')
            logger.info(f"CSV report generated successfully at {output_path}")
        except Exception as e:
            logger.error(f"Failed to generate CSV report: {e}")

    def generate_json_report(self, output_path: str = config.RESULTS_JSON_PATH) -> None:
        """
        Formats (using the provided formatter) and saves the exploration results to a JSON file.
        """
        logger.info(f"Formatting results for JSON output...")
        formatted_data = self.formatter.format(self.raw_results)
        
        logger.info(f"Generating JSON report at {output_path}")
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(formatted_data, f, ensure_ascii=False, indent=4)
            logger.info(f"JSON report generated successfully at {output_path}")
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {e}")

if __name__ == "__main__":
    test_logger = Logger(console_level=logging.DEBUG).get_logger()
    test_logger.info("--- Running ReportGenerator in stand-alone test mode ---")

    from src.data_processor import DataProcessor
    from src.data_explorer import DataExplorer
    from src.formatters import AntisemitismReportFormatter # Import the specific formatter
    
    test_logger.info("Step 1: Exploring raw data...")
    loader_processor = DataProcessor(file_path=config.INPUT_FILE_PATH)
    raw_df = loader_processor.load_csv()

    if raw_df is not None:
        explorer = DataExplorer(df=raw_df)
        exploration_results = explorer.run_full_exploration()
        test_logger.info("Raw data exploration complete.")

        test_logger.info("\n--- Step 2: Processing and Cleaning Data ---")
        cleaning_processor = DataProcessor(file_path=config.INPUT_FILE_PATH)
        cleaned_df = cleaning_processor.run_processing_pipeline()

        if cleaned_df is not None:
            test_logger.info("Data cleaning complete.")

            test_logger.info("\n--- Step 3: Generating Reports ---")
            report_generator = ReportGenerator(
                exploration_results=exploration_results,
                cleaned_df=cleaned_df,
                formatter=AntisemitismReportFormatter() # Inject the specific formatter
            )
            report_generator.generate_all_reports()
        else:
            test_logger.error("Data cleaning failed. Cannot generate reports.")
    else:
        test_logger.error("Initial data loading failed. Aborting test.")

    test_logger.info("\n--- ReportGenerator end-to-end test completed ---")