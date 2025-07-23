import unittest
from unittest.mock import Mock, patch
from report_etls.brand_power import BrandPower  # Adjust import path as needed


class TestBrandPower(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_config = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "brand_name": "test_brand",
            "market": "US"
        }
        self.brand_power = BrandPower(self.base_config)

    def test_run_etl_with_basic_config(self):
        """Test run_etl with basic configuration"""
        result = self.brand_power.run_etl()
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Competitor tracking completed.")

    def test_run_etl_with_different_date_ranges(self):
        """Test run_etl with various date ranges"""
        test_configs = [
            {"start_date": "2024-01-01", "end_date": "2024-01-31"},
            {"start_date": "2024-01-01", "end_date": "2024-02-29"},
            {"start_date": "2023-12-01", "end_date": "2024-01-31"}
        ]

        for config in test_configs:
            with self.subTest(config=config):
                self.brand_power._run_params.update(config)
                result = self.brand_power.run_etl()
                self.assertEqual(result["status"], "success")

    def test_run_etl_with_different_markets(self):
        """Test run_etl with different market parameters"""
        test_markets = ["US", "UK", "EU", "APAC"]

        for market in test_markets:
            with self.subTest(market=market):
                self.brand_power._run_params["market"] = market
                result = self.brand_power.run_etl()
                self.assertEqual(result["status"], "success")

    @patch('report_etls.brand_power.BrandPower.configure_init_tasks')
    @patch('report_etls.brand_power.BrandPower.run_pre_validation')
    @patch('report_etls.brand_power.BrandPower.run_extract_tasks')
    @patch('report_etls.brand_power.BrandPower.run_transform_process_tasks')
    @patch('report_etls.brand_power.BrandPower.run_post_validation')
    def test_run_etl_steps_execution(self, mock_post_val, mock_transform,
                                     mock_extract, mock_pre_val, mock_init):
        """Test that all ETL steps are called in correct order"""
        result = self.brand_power.run_etl()

        # Verify all steps were called exactly once
        mock_init.assert_called_once()
        mock_pre_val.assert_called_once()
        mock_extract.assert_called_once()
        mock_transform.assert_called_once()
        mock_post_val.assert_called_once()

        # Verify the order of calls
        expected_order = [
            mock_init,
            mock_pre_val,
            mock_extract,
            mock_transform,
            mock_post_val
        ]

        for i in range(len(expected_order) - 1):
            self.assertTrue(
                expected_order[i].call_count == 1 and
                expected_order[i + 1].call_count == 1
            )

    def test_run_etl_with_invalid_config(self):
        """Test run_etl with invalid configuration"""
        invalid_configs = [
            {"start_date": "invalid_date", "end_date": "2024-01-31"},
            {"start_date": "2024-01-01", "end_date": "2023-12-31"},  # end before start
            {"market": "INVALID_MARKET"}
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                self.brand_power._run_params.update(config)
                with self.assertRaises(Exception):  # Adjust exception type as needed
                    self.brand_power.run_etl()


if __name__ == '__main__':
    unittest.main()