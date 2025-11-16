import unittest
import pandas as pd
from Rank_show_duration import rank_tv_shows_by_duration

class TestRankTVShowsByDuration(unittest.TestCase):

    def setUp(self):
        self.sample_data = pd.DataFrame({
            "Title": ["Show A", "Show B", "Show C"],
            "Date": ["2020", "2019", "2021"],
            "Runtime": ["60", "45", "90"],
            "Genre": [["Drama"], ["Comedy"], ["Action"]],
            "Rating": [8.5, 7.2, 9.1]
        })

#test 1
    def test_returns_correct_top_n(self):
        result = rank_tv_shows_by_duration(self.sample_data, top_n=2)
        self.assertEqual(len(result), 2)


#test 2
    def test_sorted_by_runtime_descending(self):
        result = rank_tv_shows_by_duration(self.sample_data, top_n=3)
        runtimes = list(result["Runtime"])
        self.assertEqual(runtimes, sorted(runtimes, reverse=True))


#test 3
    def test_missing_required_columns(self):
        bad_df = pd.DataFrame({"Title": ["A"], "Genre": ["Drama"]})
        with self.assertRaises(ValueError):
            rank_tv_shows_by_duration(bad_df)


#test 4
    def test_invalid_runtime_is_dropped(self):
        df = self.sample_data.copy()
        df.loc[1, "Runtime"] = "not a number"

        result = rank_tv_shows_by_duration(df)

        self.assertEqual(len(result), 2)

#test 5
    def test_returns_expected_columns(self):
        result = rank_tv_shows_by_duration(self.sample_data)
        expected_cols = ["Title", "Date", "Runtime", "Genre", "Rating"]
        self.assertListEqual(list(result.columns), expected_cols)

if __name__ == "__main__":
    unittest.main()
