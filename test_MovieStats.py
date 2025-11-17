import unittest
import pandas as pd
from MovieStats import MovieStats

class TestMovieStats(unittest.TestCase):

    def setUp(self):
        self.sample_df = pd.DataFrame({
            "Title": ["A", "B", "C", "D"],
            "Rating": [8.5, 7.0, 9.2, 6.5],
            "Gross": [150, 300, 100, 50]
        })
        self.stats = MovieStats(self.sample_df)

#test 1
    def test_average_rating_correct(self):
        expected = (8.5 + 7.0 + 9.2 + 6.5) / 4
        self.assertAlmostEqual(self.stats.average_rating(), expected)

#test 2
    def test_average_rating_missing_column(self):
        df = pd.DataFrame({"Title": ["A"]})
        stats = MovieStats(df)
        with self.assertRaises(ValueError):
            stats.average_rating()

#test 3
    def test_average_rating_handles_non_numeric(self):
        df = pd.DataFrame({
            "Rating": ["8", "bad", "10"]
        })
        stats = MovieStats(df)
        self.assertEqual(stats.average_rating(), 9)

#test 4
    def test_average_rating_empty_numeric(self):
        df = pd.DataFrame({"Rating": ["bad", "??"]})
        stats = MovieStats(df)
        self.assertEqual(stats.average_rating(), 0)

#test 5
    def test_top_grossings_returns_dataframe(self):
        result = self.stats.top_grossings(3)
        self.assertIsInstance(result, pd.DataFrame)

#test 6
    def test_top_grossings_sorted_correctly(self):
        result = self.stats.top_grossings(3)
        self.assertEqual(list(result["Gross"]), [300, 150, 100])

#test 7
    def test_top_grossings_missing_column(self):
        df = pd.DataFrame({"Rating": [8.0]})
        stats = MovieStats(df)
        with self.assertRaises(ValueError):
            stats.top_grossings()

#test 8
    def test_top_grossings_handles_non_numeric_gross(self):
        df = pd.DataFrame({
            "Title": ["A", "B"],
            "Gross": ["100", "bad"]
        })
        stats = MovieStats(df)
        result = stats.top_grossings(2)
        self.assertEqual(list(result["Gross"]), [100])

#test 9
    def test_top_grossings_respects_n_value(self):
        result = self.stats.top_grossings(2)
        self.assertEqual(len(result), 2)

#test 10
    def test_constructor_requires_dataframe(self):
        with self.assertRaises(TypeError):
            MovieStats("not a df")


if __name__ == "__main__":
    unittest.main()
