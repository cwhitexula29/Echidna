import unittest
import requests
from xula_driver import get_centennial_campaign_impact


class TestCentennialScraper(unittest.TestCase):

    def test_valid_url_response(self):
        """
        Test 1: Ensure the URL returns a successful (200 OK) response.
        """
        url = "https://www.xula.edu/about/centennial.html"
        response = requests.get(url, timeout=10)
        
        self.assertEqual(response.status_code, 200, "URL did not return 200 OK")



    def test_impact_text_format(self):
        """
        Test 2: Check that the scraped campaign impact text is formatted correctly.
        """
        url = "https://www.xula.edu/about/centennial.html"
        result = get_centennial_campaign_impact(url)

        self.assertIsInstance(result["impact_text"], list, "impact_text should be a list")
        self.assertGreater(len(result["impact_text"]), 0, "impact_text list should not be empty")
        self.assertTrue(all(isinstance(p, str) and p.strip() for p in result["impact_text"]),
                        "All impact_text items should be non-empty strings")
        
    
   
    def test_missing_text_handling(self):
        """Test 3: If the text is not found, the function should return a fallback message."""
        fake_url = "https://www.xula.edu/nonexistent-page.html"
        result = get_centennial_campaign_impact(fake_url)

        self.assertIsInstance(result["impact_text"], list, "impact_text should still be a list")
        self.assertEqual(result["impact_text"], ["Campaign impact text not found."],
                         "Fallback message should be returned when no text found")
        
    def test_title_scraped_correctly(self):
        """
        Test 4: Ensure the page title is captured correctly.
        """
        url = "https://www.xula.edu/about/centennial.html"
        result = get_centennial_campaign_impact(url)
        
        self.assertIn("title", result, "Result should have a 'title' key")
        self.assertIsInstance(result["title"], str, "Title should be a string")
        self.assertTrue(result["title"].strip(), "Title should not be empty")


    def test_source_url_returned(self):
        """
        Test 5: Ensure the source URL is returned correctly in the result.
        """
        url = "https://www.xula.edu/about/centennial.html"
        result = get_centennial_campaign_impact(url)
        
        self.assertIn("source_url", result, "Result should have a 'source_url' key")
        self.assertEqual(result["source_url"], url, "The source URL should match the requested URL")

        #Tests added by cwhitexula29

    def test_impact_text_contains_real_content(self):
        """
        Test 6: Ensure the scraped text contains real sentences (not placeholders).
        """
        url = "https://www.xula.edu/about/centennial.html"
        result = get_centennial_campaign_impact(url)

        text = " ".join(result["impact_text"]).lower()
        self.assertGreater(len(text.split()), 5, "Impact text should contain meaningful content")


    def test_result_has_all_required_keys(self):
        """
        Test 7: Ensure the dictionary contains title, impact_text, and source_url.
        """
        url = "https://www.xula.edu/about/centennial.html"
        result = get_centennial_campaign_impact(url)

        expected_keys = {"title", "impact_text", "source_url"}
        self.assertTrue(expected_keys.issubset(result.keys()),
                        "Missing one or more required keys in the result")
        

    def test_title_contains_letters(self):
        """
        Test 8: Title should include alphabetic characters.
        """
        url = "https://www.xula.edu/about/centennial.html"
        result = get_centennial_campaign_impact(url)

        self.assertRegex(result["title"], r"[A-Za-z]", "Title should contain letters")


    def test_source_url_is_string(self):
        """
        Test 9: Confirm source_url is always stored as a string.
        """
        url = "https://www.xula.edu/about/centennial.html"
        result = get_centennial_campaign_impact(url)

        self.assertIsInstance(result["source_url"], str, "source_url must be a string")

    
    def test_malformed_html_returns_fallback(self):
        """
        Test 10: Even if the URL returns malformed or empty HTML,
        the function should return the fallback message.
        """
        bad_url = "https://www.xula.edu/thispagedoesnotexist"
        result = get_centennial_campaign_impact(bad_url)

        self.assertEqual(result["impact_text"], ["Campaign impact text not found."],
                         "Fallback text should be returned for malformed HTML")


if __name__ == "__main__":
    unittest.main()
