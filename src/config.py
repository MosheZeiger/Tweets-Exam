from pathlib import Path
import logging


"""
Configuration file for the project.

This file serves as a single source of truth for all project-wide constants,
such as file paths, directories, and model parameters.
By centralizing configuration, we ensure consistency and ease of maintenance.
This module should not import any other custom modules from this project.
"""

# ----------------
# Paths configuration
# ----------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
RESULTS_DIR = PROJECT_ROOT / 'results'
LOGS_DIR = PROJECT_ROOT / 'logs'


# ----------------
# Data configuration
# ----------------
CSV_ENCODING = 'latin-1'
CLASSIFICATION_COLUMN = 'Biased'
TEXT_COLUMN = 'Text'
RELEVANT_COLUMNS = ['Text', 'Biased']
CATEGORY_MAPPING = {
}


# -----------------
# ANALYSIS CONFIGURATION
# -----------------
TOP_N_LONGEST_TWEETS = 3
TOP_N_COMMON_WORDS = 10

# ----------------
# Logging configuration
# ----------------
LOG_NAME = 'AntisemitismAnalysisLogger.log'
LOG_MAIN_LEVEL = logging.DEBUG
LOG_FILE_LEVEL = logging.INFO
LOG_CONSOLE_LEVEL = logging.ERROR
