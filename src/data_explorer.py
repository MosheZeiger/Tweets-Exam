import pandas as pd
from src.logger import Logger
from src import config
import logging
import pprint
import re

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

    def get_count_by_category(self, category_column: str) -> dict:
        if category_column not in self.df.columns:
            logger.error(f"Column '{category_column}' does not exist in DataFrame.")
            return {}
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
        final_counts['total'] = len(self.df)
        self.exploration_results['category_counts'] = final_counts
        return final_counts
    
    def calculate_average_word_count(self, text_column: str, category_column: str) -> dict:
        if text_column not in self.df.columns or category_column not in self.df.columns:
            logger.error(f"One or both columns ('{text_column}', '{category_column}') not found.")
            return {}
        logger.info(f"Calculating average word count for '{text_column}' grouped by '{category_column}'")
        temp_df = self.df.copy()
        temp_df[text_column] = temp_df[text_column].fillna('')
        temp_df['word_count'] = temp_df[text_column].str.split().str.len()
        total_average = temp_df['word_count'].mean()
        category_averages = temp_df.dropna(subset=[category_column]).groupby(category_column)['word_count'].mean().to_dict()
        avg_lengths = {'total': round(total_average, 2)}
        for category, avg in category_averages.items():
            if isinstance(category, float) and category.is_integer():
                key = str(int(category))
            else:
                key = str(category)
            avg_lengths[key] = round(avg, 2)
        self.exploration_results['average_length'] = avg_lengths
        return avg_lengths
    
    def get_n_longest_texts_by_category(self, text_column: str, category_column: str, n: int = 3) -> dict:
        if text_column not in self.df.columns or category_column not in self.df.columns:
            logger.error(f"One or both columns ('{text_column}', '{category_column}') not found.")
            return {}
        logger.info(f"Finding {n} longest texts by word count for each category in '{category_column}'")
        temp_df = self.df.copy()
        temp_df.dropna(subset=[text_column, category_column], inplace=True)
        temp_df['word_count'] = temp_df[text_column].str.split().str.len()
        temp_df = temp_df.sort_values(by='word_count', ascending=False)
        longest_texts_df = temp_df.groupby(category_column).head(n)
        longest_texts_dict = {}
        for category, group in longest_texts_df.groupby(category_column):
            if isinstance(category, float) and category.is_integer():
                key = str(int(category))
            else:
                key = str(category)
            longest_texts_dict[key] = group[text_column].tolist()
        self.exploration_results['longest_texts_by_category'] = longest_texts_dict
        return longest_texts_dict
    

    def get_most_common_words(self, text_column: str, n: int = 10) -> list:
        """
        Finds the n most common words in the specified text column.
        """
        if text_column not in self.df.columns:
            logger.error(f"Column '{text_column}' does not exist in DataFrame.")
            return []
        
        logger.info(f"Finding {n} most common words in column: {text_column}")

        text_series = self.df[text_column].dropna()
        text_series = text_series.str.lower()
        text_series = text_series.str.replace(r'[^\w\s]', '', regex=True)
        full_text = ' '.join(text_series)
        words = full_text.split()

        if not words:
            return []
        word_counts = pd.Series(words).value_counts()
        most_common = word_counts.head(n).index.tolist()

        logger.info(f"Most common words found: {most_common}")
        self.exploration_results['most_common_words'] = most_common
        return most_common
    
    def count_uppercase_words_by_category(self, text_column: str, category_column: str) -> dict:
        """
        Counts the number of uppercase words in the specified text column
        """
        if text_column not in self.df.columns or category_column not in self.df.columns:
            logger.error(f"One or both columns ('{text_column}', '{category_column}') not found.")
            return {}

        logger.info(f"Counting uppercase words in '{text_column}', grouped by '{category_column}'.")

        temp_df = self.df.copy()
        temp_df[text_column] = temp_df[text_column].fillna('')
        
        def _count_uppercase(text: str) -> int:
            if not isinstance(text, str):
                return 0
            return sum(1 for word in text.split() if word.isupper())
        
        temp_df['uppercase_word_count'] = temp_df[text_column].apply(_count_uppercase)

        total_uppercase_words = int(temp_df['uppercase_word_count'].sum())

        category_uppercase_counts = temp_df.dropna(
            subset=[category_column]
        ).groupby(category_column)['uppercase_word_count'].sum().astype(int).to_dict()

        final_results = {'total': total_uppercase_words}

        for category, count in category_uppercase_counts.items():
            if isinstance(category, float) and category.is_integer():
                key = str(int(category))
            else:
                key = str(category)
            final_results[key] = count

        logger.info(f"Uppercase word counts calculated: {final_results}")
        self.exploration_results['uppercase_words_count'] = final_results
        
        return final_results

    def run_full_exploration(self) -> dict:
        """
        Runs all exploration methods and returns the consolidated results.
        """
        logger.info("Starting full data exploration.")
        self.get_count_by_category(category_column=config.CLASSIFICATION_COLUMN)
        self.calculate_average_word_count(
            text_column=config.TEXT_COLUMN,  
            category_column=config.CLASSIFICATION_COLUMN
        )
        self.get_n_longest_texts_by_category(
            text_column=config.TEXT_COLUMN,
            category_column=config.CLASSIFICATION_COLUMN,
            n=config.TOP_N_LONGEST_TWEETS
        )
        self.get_most_common_words(
            text_column=config.TEXT_COLUMN,
            n=config.TOP_N_COMMON_WORDS
        )
        self.count_uppercase_words_by_category(
            text_column=config.TEXT_COLUMN,
            category_column=config.CLASSIFICATION_COLUMN
        )
        logger.info("Data exploration completed.")
        logger.info("Data exploration completed.")
        return self.exploration_results


if __name__ == "__main__":
    from src.data_processor import DataProcessor
    test_logger = Logger(console_level=logging.DEBUG).get_logger()
    test_logger.info("=== Starting DataExplorer Test ===")
    input_file = config.DATA_DIR / 'tweets_dataset.csv'
    processor = DataProcessor(file_path=input_file)
    raw_df = processor.load_csv()

    if raw_df is not None:
        explorer = DataExplorer(df=raw_df)
        
        test_logger.info("\n--- Testing run_full_exploration ---")
        all_results = explorer.run_full_exploration()
        test_logger.info("Consolidated exploration results gathered by run_full_exploration:")
        pprint.pprint(all_results)
    else:
        test_logger.error("Failed to load DataFrame. Aborting tests.")
    
    test_logger.info("=== DataExplorer Test Completed ===")