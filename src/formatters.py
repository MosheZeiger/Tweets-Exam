from src import config

class BaseFormatter:
    """
    Base class for report formatters. Subclasses should implement the format method.
    """
    def format(self, raw_results: dict) -> dict:
        # Default formatter does nothing, just returns the data as is.
        return raw_results

class AntisemitismReportFormatter(BaseFormatter):
    """
    Formats the raw exploration results into the specific structure
    required for the antisemitism analysis report.
    """
    def format(self, raw_results: dict) -> dict:
        category_map = {
            '0': 'non_antisemitic',
            '1': 'antisemitic',
            'unclassified': 'unspecified',
            'total': 'total'
        }

        formatted_dict = {}

        # Format tweet counts
        raw_counts = raw_results.get('category_counts', {})
        formatted_dict['total_tweets'] = {
            category_map.get(str(k), k): v for k, v in raw_counts.items()
        }

        # Format average length
        raw_avg_len = raw_results.get('average_length', {})
        formatted_dict['average_length'] = {
            category_map.get(str(k), k): v for k, v in raw_avg_len.items()
        }

        # Format longest tweets
        raw_longest = raw_results.get('longest_texts_by_category', {})
        longest_key_name = f"longest_{config.TOP_N_LONGEST_TWEETS}_tweets"
        formatted_dict[longest_key_name] = {
            category_map.get(str(k), k): v for k, v in raw_longest.items()
        }

        # Format common words
        formatted_dict['common_words'] = {
            'total': raw_results.get('most_common_words', [])
        }

        # Format uppercase words count
        raw_uppercase = raw_results.get('uppercase_words_count', {})
        formatted_dict['uppercase_words'] = {
            category_map.get(str(k), k): v for k, v in raw_uppercase.items()
        }

        return formatted_dict