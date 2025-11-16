import random

class FakeMovie:
    def __init__(self):
        self.titles = ["Hidden Truth", "Starlight Echo", "The Last Horizon", "Midnight Pulse", "Broken Reality"]
        self.genres = ["Drama", "Comedy", "Action", "Sci-Fi", "Adventure", "Thriller"]
        self.years = ["1999", "2005", "2010", "2017", "2022"]
        self.ratings = [6.2, 7.8, 8.1, 5.9, 9.0]

    def generate_movie(self):
        return {
            "Title": random.choice(self.titles),
            "Genre": random.choice(self.genres),
            "Date": random.choice(self.years),
            "Rating": random.choice(self.ratings)
        }