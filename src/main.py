from src.logger import Logger
from src import config
from src.data_processor import DataProcessor
from src.data_explorer import DataExplorer
from src.report_generator import ReportGenerator
from src.formatters import AntisemitismReportFormatter

def main():
    """
    The main function to run the entire analysis and reporting pipeline.
    """
    logger = Logger(
        name=config.LOG_NAME,
        logs_dir=config.LOGS_DIR.name,
        main_level=config.LOG_MAIN_LEVEL,
        file_level=config.LOG_FILE_LEVEL,
        console_level=config.LOG_CONSOLE_LEVEL
    ).get_logger()
    
    logger.info("========================================")
    logger.info("Application starting...")
    logger.info(f"Input data file: {config.INPUT_FILE_PATH}")
    logger.info("========================================")

    # --- Step 1: Exploratory Data Analysis (on raw data) ---
    logger.info("--- Running Step 1: Exploratory Data Analysis ---")
    # We use a DataProcessor instance just to load the raw data
    loader_for_exploration = DataProcessor(file_path=config.INPUT_FILE_PATH)
    raw_df = loader_for_exploration.load_csv()
    
    if raw_df is None:
        logger.error("Fatal: Could not load raw data. Exiting application.")
        return

    explorer = DataExplorer(df=raw_df)
    exploration_results = explorer.run_full_exploration()
    logger.info("Step 1 finished: Raw data exploration complete.")

    # --- Step 2: Data Processing and Cleaning ---
    logger.info("\n--- Running Step 2: Data Processing and Cleaning ---")
    # We create a new DataProcessor instance to run the full cleaning pipeline
    cleaning_processor = DataProcessor(file_path=config.INPUT_FILE_PATH)
    cleaned_df = cleaning_processor.run_processing_pipeline()

    if cleaned_df is None:
        logger.error("Fatal: Data processing pipeline failed. Exiting application.")
        return

    logger.info("Step 2 finished: Data cleaning complete.")

    # --- Step 3: Report Generation ---
    logger.info("\n--- Running Step 3: Generating Final Reports ---")
    # We create our specific formatter for this project
    report_formatter = AntisemitismReportFormatter()
    # We initialize the report generator with all the results
    report_generator = ReportGenerator(
        exploration_results=exploration_results,
        cleaned_df=cleaned_df,
        formatter=report_formatter
    )
    report_generator.generate_all_reports()
    logger.info("Step 3 finished: All reports generated.")

    logger.info("========================================")
    logger.info("Application finished successfully.")
    logger.info(f"Output files are located in: {config.RESULTS_DIR}")
    logger.info("========================================")

if __name__ == "__main__":
    main()