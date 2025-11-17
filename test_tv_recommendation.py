import unittest
import pandas as pd
from tv_recommendation import TVShowRecommender

class TestTVShowRecommender(unittest.TestCase):

    def setUp(self):
        self.sample_df = pd.DataFrame({
            "Title": ["Show A", "Show B", "Show C"],
            "Date": ["2020", "2019", "2021"],
            "Genre": [["Drama"], ["Comedy"], ["Action"]],
            "Rating": [8.5, 7.2, 9.1]
        })

        self.recommender = TVShowRecommender(self.sample_df)

#test 1
    def test_returns_dictionary(self):
        result = self.recommender.recommend_show()
        self.assertIsInstance(result, dict, "recommend_show() should return a dictionary")

#test 2
    def test_empty_dataframe_returns_error(self):
        empty_df = pd.DataFrame()
        rec = TVShowRecommender(empty_df)
        result = rec.recommend_show()
        self.assertIn("Error", result)
        self.assertEqual(result["Error"], "TV DataFrame is empty")

#test 3
    def test_result_has_required_keys(self):
        result = self.recommender.recommend_show()
        expected = {"Title", "Date", "Genre", "Rating"}
        self.assertTrue(expected.issubset(result.keys()))

#test 4
    def test_values_match_dataframe(self):
        result = self.recommender.recommend_show()
        self.assertIn(result["Title"], list(self.sample_df["Title"]))
        self.assertIn(result["Date"], list(self.sample_df["Date"]))
        self.assertIn(result["Genre"], list(self.sample_df["Genre"]))
        self.assertIn(result["Rating"], list(self.sample_df["Rating"]))

#test 5
    def test_randomness_over_multiple_runs(self):
        results = {self.recommender.recommend_show()["Title"] for _ in range(10)}
        self.assertGreater(len(results), 1, "Recommendations should vary randomly")

if __name__ == "__main__":
    unittest.main()
