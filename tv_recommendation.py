import random

class TVShowRecommender:
    
    def __init__(self, tv_df):
        self.tv_df = tv_df

    def recommend_show(self):
        if self.tv_df.empty:
            return {"Error": "TV DataFrame is empty"}

        random_index = random.randint(0, len(self.tv_df) - 1)
        show = self.tv_df.iloc[random_index]

        return {
            "Title": show.get("Title", "N/A"),
            "Date": show.get("Date", "N/A"),
            "Genre": show.get("Genre", "N/A"),
            "Rating": show.get("Rating", "N/A")
        }
