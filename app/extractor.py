import requests
import pandas as pd
from io import StringIO
import logging
from tqdm import tqdm

class TVPExtractor:
    def __init__(self, api_key, log_file="tvp_extractor.log"):
        """
        Initialize the extractor with the Dune API key and set up logging.
        """
        self.api_key = api_key
        self.base_url = "https://api.dune.com/api/v1/query"

        # Set up logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("TVPExtractor initialized.")

    def fetch_tvp_data(self, query_id, limit=1000, max_pages=None):
        """
        Fetch TVP data from the Dune API, handling pagination for large datasets.
        
        Args:
            query_id (int): The ID of the Dune query to execute.
            limit (int): The number of rows to fetch per API call (default 1000).
            max_pages (int): The maximum number of pages to fetch (optional, for testing or limits).
        
        Returns:
            pd.DataFrame: The raw data as a consolidated Pandas DataFrame.
        """
        headers = {"X-Dune-API-Key": self.api_key}
        offset = 0
        all_data = []  # To store each batch of fetched data
        total_pages = max_pages or 10_000  # Default large number if max_pages not specified

        # Initialize progress bar
        with tqdm(total=total_pages, desc="Fetching Data", unit="batch") as pbar:
            while True:
                url = f"{self.base_url}/{query_id}/results/csv?limit={limit}&offset={offset}"
                self.logger.info(f"Fetching data with offset {offset}...")
                
                try:
                    # API Request
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()  # Check for HTTP errors

                    # Convert the CSV response to a Pandas DataFrame
                    csv_data = StringIO(response.text)
                    batch_data = pd.read_csv(csv_data)

                    # If no data is returned, break the loop
                    if batch_data.empty:
                        self.logger.info("No more data to fetch.")
                        break

                    all_data.append(batch_data)
                    offset += limit  # Move to the next batch
                    pbar.update(1)  # Update progress bar
                    
                    # Stop after max_pages if defined
                    if max_pages and len(all_data) >= max_pages:
                        self.logger.info(f"Reached maximum defined pages: {max_pages}.")
                        break
                
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"Error fetching data from Dune: {e}")
                    break
                except Exception as e:
                    self.logger.exception(f"Unexpected error: {e}")
                    break

        # Concatenate all batches into a single DataFrame
        if all_data:
            final_data = pd.concat(all_data, ignore_index=True)
            self.logger.info(f"Data successfully fetched and consolidated: {len(final_data)} rows.")
            return final_data
        else:
            self.logger.warning("No data fetched.")
            return None
