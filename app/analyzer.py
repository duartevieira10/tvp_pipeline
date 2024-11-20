from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum
from extractor import TVPExtractor  


class TVPAnalyzer:
    def __init__(self, spark_session, extractor=None, vertical_data=None, protocol_data=None):
        """
        Initialize the analyzer with paths to vertical and protocol data or a TVPExtractor instance.
        
        Args:
            spark_session (SparkSession): Spark session for distributed processing.
            extractor (TVPExtractor): An instance of TVPExtractor for fetching data.
            vertical_path (str): Path to the vertical summary Parquet file.
            protocol_path (str): Path to the protocol summary Parquet file.
        """

        self.spark = spark_session
        self.extractor = extractor
        self.vertical_data = None
        self.protocol_data = None

        if vertical_data and protocol_data:
            self.vertical_data = self.load_parquet(vertical_data)
            self.protocol_data = self.load_parquet(protocol_data)

    def load_parquet(self, path):
        return self.spark.read.parquet(path)
    
    def fetch_from_dune(self, query_id):
        """
        Fetch data from Dune using the TVPExtractor and load into a Spark DataFrame.
        
        Args:
            query_id (int): Dune query ID.
        
        Returns:
            DataFrame: Spark DataFrame with fetched data.
        """

        if not self.extractor:
            raise ValueError("TVPExtractor instance is not provided.")
        
        data = self.extractor.fetch_tvp_data(query_id)

        if data is not None:
            return self.spark.createDataFrame(data)
        else:
            raise ValueError(f"Failed to fetch data from Dune for query ID: {query_id}")
        
    def get_top_k_verticals(self, k=5):
        """
        Identify the top K verticals by transaction volume and count.
        
        Args:
            k (int): Number of top verticals to return.
        
        Returns:
            dict: Two Spark DataFrames containing the top K verticals by volume and count.
        """

        if not self.vertical_data:
            raise ValueError("Vertical data is not loaded.")
        
        top_volume = (
            self.vertical_data
            .groupBy("vertical")
            .agg(spark_sum("total_tvp_usd").alias("total_volume"))
            .orderBy(col("total_volume").desc())
            .limit(k)
        )

        top_count = (
            self.vertical_data
            .groupBy("vertical")
            .agg(spark_sum("total_transactions").alias("total_count"))
            .orderBy(col("total_count").desc())
            .limit(k)
        )

        return {"top_volume": top_volume, "top_count": top_count}
    
    def get_top_k_protocols(self, k=5):
        """
        Identify the top K protocols by transaction volume and count.
        
        Args:
            k (int): Number of top protocols to return.
        
        Returns:
            dict: Two Spark DataFrames containing the top K protocols by volume and count.
        """

        if not self.protocol_data:
            raise ValueError("Protocol data is not loaded.")
        
        top_volume = (
            self.protocol_data
            .groupBy("protocol")
            .agg(spark_sum("total_tvp_usd").alias("total_volume"))
            .orderBy(col("total_volume").desc())
            .limit(k)
        )

        top_count = (
            self.protocol_data
            .groupBy("protocol")
            .agg(spark_sum("total_transactions").alias("total_count"))
            .orderBy(col("total_count").desc())
            .limit(k)
        )

        return {"top_volume": top_volume, "top_count": top_count}
    





        

