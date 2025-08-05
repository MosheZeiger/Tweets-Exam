from src.logger import Logger
from src import config


def initialize_app():
    logger_instance = Logger(
        name=config.LOG_NAME,
        logs_dir=config.LOGS_DIR.name,
        main_level=config.LOG_MAIN_LEVEL,
        file_level=config.LOG_FILE_LEVEL,
        console_level=config.LOG_CONSOLE_LEVEL
    )
    return logger_instance.get_logger()


def main():
    logger = initialize_app()
    logger.info("========================================")
    logger.info("Application started successfully.")
    logger.info("========================================")



if __name__ == "__main__":
    main()