import pandas as pd
import os
import requests


output_directory = os.getenv("OUTPUT_DIRECTORY", "output")

class TVPLoader:
    def __init__(self, output_directory=output_directory):
        """
        Initialize the loader with an output directory.

        Args:
            output_directory (str): Directory to store the output files.
        """
        self.output_directory = output_directory
        os.makedirs(output_directory, exist_ok=True)

    def save_to_parquet(self, data, filename):
        """
        Save a DataFrame to a Parquet file.

        Args:
            data (pd.DataFrame): The DataFrame to save.
            filename (str): Name of the Parquet file
        """
        filepath = os.path.join(self.output_directory, f"{filename}.parquet") #filename
        data.to_parquet(filepath, index=False)
        print(f"Data saved to Parquet: {filepath}")

    def upload_to_dune(self, data, api_key, table_name):
        """
        Upload a DataFrame to a Dune table.
        
        Args:
            data (pd.DataFrame): The DataFrame to upload.
            dune_api_key (str): API key for Dune.
            table_name (str): Target Dune table name.
        """
        url = f"https://api.dune.com/api/v1/table/{table_name}"
        headers = {"X-Dune-API-Key": api_key, "Content-Type": "application/json"}
        payload = data.to_json(orient='records')

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            print(f"Data uploaded to Dune table '{table_name}'.")

        except requests.exceptions.RequestException as e:
            print(f"Error uploading data to Dune: {e}")



