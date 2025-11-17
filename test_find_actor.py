import unittest
import pandas as pd
from xula_driver import find_movie_by_actor

class TestFindMovieByActor(unittest.TestCase):

    def setUp(self):
        self.sample_df = pd.DataFrame({
            "Title": ["Movie A", "Movie B", "Movie C"],
            "Stars": [
                ["John Smith", "Alice Brown"],
                ["David Lee", "Chris Stone"],
                ["Alice Brown", "Michael Bay"]
            ],
            "Rating": [8.1, 7.3, 9.0]
        })

#test 1
    def test_actor_found_multiple_movies(self):
        result = find_movie_by_actor(self.sample_df, "Alice Brown")
        self.assertEqual(len(result), 2)

#test 2
    def test_actor_found_once(self):
        result = find_movie_by_actor(self.sample_df, "David Lee")
        self.assertEqual(len(result), 1)

#test 3
    def test_actor_not_found(self):
        result = find_movie_by_actor(self.sample_df, "Tom Cruise")
        self.assertTrue(result.empty)

#test 4
    def test_case_insensitive_search(self):
        result = find_movie_by_actor(self.sample_df, "alice brown")
        self.assertEqual(len(result), 2)

#test 5
    def test_stars_not_list(self):
        df = self.sample_df.copy()
        df.loc[1, "Stars"] = "not a list"
        
        result = find_movie_by_actor(df, "Chris Stone")
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()