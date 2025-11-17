import pandas as pd

class MovieStats:
    def __init__(self, df: pd.DataFrame):
        
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")
        self.df = df

    def average_rating(self):
        """Return the average rating of all movies."""
        if "Rating" not in self.df.columns:
            raise ValueError("DataFrame must contain 'Rating' column")
        
        numeric_ratings = pd.to_numeric(self.df["Rating"], errors="coerce")
        numeric_ratings = numeric_ratings.dropna()

        if numeric_ratings.empty:
            return 0  

        return numeric_ratings.mean()

    def top_grossings(self, n=5):
        """Return the top n movies sorted by Gross revenue."""
        if "Gross" not in self.df.columns:
            raise ValueError("DataFrame must contain 'Gross' column")

        temp_df = self.df.copy()
        temp_df["Gross"] = pd.to_numeric(temp_df["Gross"], errors="coerce")
        temp_df = temp_df.dropna(subset=["Gross"])

        return temp_df.sort_values(by="Gross", ascending=False).head(n)