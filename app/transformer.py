import pandas as pd


class TVPTransformer:
    def __init__(self, raw_data):
        """
        Initialize the transformer with raw data.
        
        Args:
            raw_data (pd.DataFrame): The raw TVP data.
        """
        self.raw_data = raw_data
    
    @staticmethod
    def convert_to_week(date_column):
        """
        Convert a date column to ISO week format (YYYY-WW).

        Args:
            date_column (pd.Series): Column with date values.
        
        Returns:
            pd.Series: Column with week values.
        """
        return pd.to_datetime(date_column).dt.strftime('%Y-%U')
    
    def summarize_by_week_and_vertical(self):
        """
        Summarize TVP data by week and vertical.
        
        Returns:
            pd.DataFrame: Summary with unique Safes, transaction counts, and outgoing TVP per week and vertical.
        """

        self.raw_data['week'] = self.convert_to_week(self.raw_data['block_date'])

        summary = (
            self.raw_data
            .groupby(['week', 'vertical', 'safe_sender'])
            .agg(
                total_transactions = ('tx_hash', 'count'),
                total_tvp_usd = ( 'amount_usd', 'sum')
            )
            .reset_index()
            .groupby(['week', 'vertical'])
            .agg(
                unique_safes = ('safe_sender', 'nunique'),
                total_transactions = ('total_transactions', 'sum'),
                total_tvp_usd = ('total_tvp_usd', 'sum')
            )
            .reset_index()
        )

        return summary
    
    def summarize_by_week_and_protocol(self):
        """
        Summarize TVP data by week and protocol.
        
        Returns:
            pd.DataFrame: Summary with unique Safes, transaction counts, and outgoing TVP per week and protocol.
        """

        self.raw_data['week'] = self.convert_to_week(self.raw_data['block_date'])

        summary = (
            self.raw_data
            .groupby(['week', 'protocol', 'safe_sender'])
            .agg(
                total_transactions = ('tx_hash', 'count'),
                total_tvp_usd = ( 'amount_usd', 'sum')
            )
            .reset_index()
            .groupby(['week', 'protocol'])
            .agg(
                unique_safes = ('safe_sender', 'nunique'),
                total_transactions = ('total_transactions', 'sum'),
                total_tvp_usd = ('total_tvp_usd', 'sum')
            )
            .reset_index()
        )

        return summary

