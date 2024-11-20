from extractor import TVPExtractor
from transformer import TVPTransformer
from loader import TVPLoader
from analyzer import TVPAnalyzer
from pyspark.sql import SparkSession
import os
import pandas as pd


# Load environment variables
api_key = os.getenv("DUNE_API_KEY")
query_id = int(os.getenv("QUERY_ID"))
output_directory = os.getenv("OUTPUT_DIRECTORY", "output")

def main():
   # Step 1: Extract data

    extractor = TVPExtractor(api_key)
    raw_data = extractor.fetch_tvp_data(query_id, limit=1000)

    # To run locally
    # file_path = 'raw_tvp_data.csv'
    # raw_data = pd.read_csv(file_path)

    if raw_data is not None:
        print(f"Raw data fetched: {len(raw_data)} rows.")

        # Step 2: Transform data
        transformer = TVPTransformer(raw_data)
        weekly_vertical_summary = transformer.summarize_by_week_and_vertical()
        weekly_protocol_summary = transformer.summarize_by_week_and_protocol()

        # Step 3: Load data
        loader = TVPLoader(output_directory=output_directory)
        loader.save_to_parquet(weekly_vertical_summary, "weekly_vertical_summary")
        loader.save_to_parquet(weekly_protocol_summary, "weekly_protocol_summary")

        # Optionally upload to Dune
        dune_table_name = "processed_tvp_data"
        loader.upload_to_dune(weekly_vertical_summary, api_key, dune_table_name)
        loader.upload_to_dune(weekly_protocol_summary, api_key, dune_table_name)

        # Step 4: Analyse data
        # Initialize Spark session
        spark = SparkSession.builder \
            .appName("TVP Analysis") \
            .getOrCreate()

        # File paths or Dune query IDs
        vertical_data_path = "output/weekly_vertical_summary.parquet"
        protocol_data_path = "output/weekly_protocol_summary.parquet"

        # Load data from Parquet or Dune
        analyzer = TVPAnalyzer(
            spark,
            vertical_data = vertical_data_path,
            protocol_data = protocol_data_path,
    #       api_key = api_key
        )

        # Fetch Dune data if necessary
        # analyzer.vertical_df = analyzer.fetch_from_dune(vertical_query_id)
        # analyzer.protocol_df = analyzer.fetch_from_dune(protocol_query_id)

        # Analyze top verticals
        top_verticals = analyzer.get_top_k_verticals(k=5)
        print("Top 5 Vertical by Transaction Volume:")
        top_verticals["top_volume"].show()
        print("\nTop 5 Vertical by Transaction Count:")
        top_verticals["top_count"].show()

        # Analyze top protocols
        top_protocols = analyzer.get_top_k_protocols(k=5)
        print("Top 5 Protocols by Transaction Volume:")
        top_protocols["top_volume"].show()
        print("\nTop 5 Protocols by Transaction Count:")
        top_protocols["top_count"].show()

        # Stop Spark session
        spark.stop()

    else:
        print("Failed to fetch data. Check logs for details.")

if __name__ == "__main__":
    main()

    

    


