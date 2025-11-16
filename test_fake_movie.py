import unittest
from fake_movie import FakeMovie

class TestFakeMovie(unittest.TestCase):

    def setUp(self):
        self.fake = FakeMovie()


#test 1
    def test_generate_movie_returns_dict(self):
        movie = self.fake.generate_movie()
        self.assertIsInstance(movie, dict, "generate_movie() should return a dictionary")

#test 2
    def test_movie_has_required_keys(self):
        movie = self.fake.generate_movie()
        expected_keys = {"Title", "Genre", "Date", "Rating"}
        self.assertTrue(expected_keys.issubset(movie.keys()),
                        "Movie dictionary must contain Title, Genre, Date, Rating")
        
#test 3
    def test_values_are_from_defined_lists(self):
        movie = self.fake.generate_movie()
        self.assertIn(movie["Title"], self.fake.titles)
        self.assertIn(movie["Genre"], self.fake.genres)
        self.assertIn(movie["Date"], self.fake.years)
        self.assertIn(movie["Rating"], self.fake.ratings)

#test 4
    def test_randomness_over_multiple_runs(self):
        results = {self.fake.generate_movie()["Title"] for _ in range(10)}
        self.assertGreater(len(results), 1, "Generated movies should show variation (randomness)")

#test 5
    def test_rating_is_float_or_int(self):
        movie = self.fake.generate_movie()
        self.assertIsInstance(movie["Rating"], (float, int), "Rating must be numeric")

if __name__ == "__main__":
    unittest.main()