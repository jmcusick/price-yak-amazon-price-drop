import unittest
import jmc.frugal.auction_house.price_scraper as price_scraper

from unittest import mock

class TestPriceScraper(unittest.TestCase):

    @mock.patch('jmc.frugal.auction_house.price_scraper.requests')
    def test_get_cheapest_offer(self, mock_requests):
        # Given
        mock_resp = {
            "timestamp": 1566094304,
            "offers": [
                {
                    "seller": {
                        "name": "CHEAP",
                        "id": "A19N59FKNWHX7C",
                    },
                    "offer_id": "JbaNgGfY2tdpbQajW1QpVBSYryhWHu99ttlI1Q5E2%2BaSdZvJiK2LcwhNDIZ6Iz20UuM%2Bj9%2FyL5lM9wc%2Ft9DJ%2B7MXxNcx09QtxQTsPu1IgkFFXpmi7Ej3F4cIPWoGl5uNcuXTj5PIR%2FFCCJWaKk004w%3D%3D",
                    "price": 101,
                    "currency": "USD",
                    "asin": "B07EX"
                },
                {
                    "seller": {
                        "name": "EXPENSIVE",
                        "id": "A19N59FKNWHX7C",
                    },
                    "offer_id": "JbaNgGfY2tdpbQajW1QpVBSYryhWHu99ttlI1Q5E2%2BaSdZvJiK2LcwhNDIZ6Iz20UuM%2Bj9%2FyL5lM9wc%2Ft9DJ%2B7MXxNcx09QtxQTsPu1IgkFFXpmi7Ej3F4cIPWoGl5uNcuXTj5PIR%2FFCCJWaKk004w%3D%3D",
                    "price": 39911,
                    "currency": "USD",
                    "asin": "B07EX"
                  }
            ]
        }

        mock_requests.get.return_value.json.return_value = mock_resp

        # When
        offer = price_scraper.get_cheapest_offer("B07EX")

        # Then
        mock_requests.get.assert_called_once()
        assert offer.price == 101
        assert offer.seller_name == "CHEAP"
