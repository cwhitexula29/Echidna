import pandas as pd

class DirecrtorFilter:
    def __init__(self, movies_df):
        """
        movies_df: pandas DataFrame containing movie data
        Expected column: 'Director'
        """
        self.movies_df = movies_df

    def filter_by_director(self, director_name):
        """
        Returns all movies directed by the specified director.
        """
        
        if self.movies_df.empty:
            raise ValueError("The movies DataFrame is empty.")
        
        filtered = self.movies_df[self.movies_df['Director'].str.lower() == director_name.lower()]

        if filtered.empty:
            return f"No movies found for director: {director_name}"
        return filtered