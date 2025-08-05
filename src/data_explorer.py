import pandas as pd
from src.logger import Logger
from src import config
import logging

logger = Logger().get_logger()

class DataExplorer:
    """
    Performs exploratory data analysis (EDA) on a pandas DataFrame.
    This class is responsible for gathering initial statistics and insights
    in a generic, reusable way.
    """

    def __init__(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            logger.error("Input is not a pandas DataFrame.")
            raise TypeError("Input must be a pandas DataFrame.")
        self.df = df
        self.exploration_results = {}
        logger.info(f"DataExplorer initialized with DataFrame of shape: {self.df.shape}")

    def get_count_by_category(self, category_column: str) -> pd.Series:
        """
        Returns the count of unique values in the specified category column.
        """
        if category_column not in self.df.columns:
            logger.error(f"Column '{category_column}' does not exist in DataFrame.")
            raise ValueError(f"Column '{category_column}' does not exist in DataFrame.")
        
        logger.info(f"Counting unique values in column: {category_column}")
        counts = self.df[category_column].value_counts(dropna=False).to_dict()

        final_counts = {}
        for key, value in counts.items():
            if pd.isna(key):
                new_key = 'unclassified'
            elif isinstance(key, float) and key.is_integer():
                new_key = str(int(key))
            else:
                new_key = str(key)
            final_counts[new_key] = value
        
        final_counts['Total'] = len(self.df)

        logger.info(f"Count by category for '{category_column}': {final_counts}")
        self.exploration_results[category_column] = final_counts
        return final_counts
    
    