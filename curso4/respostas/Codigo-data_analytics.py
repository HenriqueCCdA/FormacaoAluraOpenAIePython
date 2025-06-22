
import pandas as pd

class DataAnalytics:

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.cache = {}

    def get_top_channel_by_viewers(self, top_n=10) -> pd.Series:
        """
        Get the top N channels by viewing time.
        
        Parameters:
        top_n (int): Number of top channels to return.
        
        Returns:
        pd.Series: Series containing top N channels with highest viewing time.
        """
        return self.data.groupby('Channel')['Watch time(Minutes)'].sum().nlargest(top_n)
