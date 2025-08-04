import unittest
import json
import os
import tempfile
from unittest.mock import Mock, patch
from report_etls.brand_power import BrandPower, CompanyDataResponse


class TestBrandPower(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_config = {
            "target_industries": ["Technology"],
            "company_name": "test_company",
            "description_of_company": "Test company description",
            "company_website": "www.testcompany.com",
            "location": "Test Location",
            "known_competitors": ["competitor1", "competitor2"]
        }
        self.llm_service_manager = Mock()
        self.brand_power = BrandPower(
            self.base_config, self.llm_service_manager
        )
        # Set up temporary directory for cache tests
        self.temp_dir = tempfile.mkdtemp()
        self.temp_cache_file = os.path.join(self.temp_dir, "test_cache.json")

    def test_init_with_valid_config(self):
        """Test initialization with valid configuration"""
        brand_power = BrandPower(self.base_config, self.llm_service_manager)
        self.assertIsNotNone(brand_power)

    def test_check_run_params_with_valid_config(self):
        """Test run parameter validation with valid configuration"""
        result = self.brand_power._BrandPower__check_run_params()
        self.assertIsNone(result)  # Should pass without raising exceptions

    def test_check_run_params_with_missing_fields(self):
        """Test run parameter validation with missing fields"""
        invalid_config = {
            "target_industries": ["Technology"]
            # Missing other required fields
        }
        brand_power = BrandPower(invalid_config, self.llm_service_manager)
        with self.assertRaises(ValueError) as context:
            brand_power._BrandPower__check_run_params()
        self.assertTrue(
            "Missing required run parameters" in str(context.exception)
        )

    def test_check_run_params_with_empty_fields(self):
        """Test run parameter validation with empty fields"""
        invalid_config = self.base_config.copy()
        invalid_config["company_name"] = ""  # Empty field
        brand_power = BrandPower(invalid_config, self.llm_service_manager)
        with self.assertRaises(ValueError) as context:
            brand_power._BrandPower__check_run_params()
        self.assertTrue("cannot be empty" in str(context.exception))

    def test_check_run_params_with_invalid_industry(self):
        """Test run parameter validation with invalid industry"""
        invalid_config = self.base_config.copy()
        invalid_config["target_industries"] = ["InvalidIndustry"]
        brand_power = BrandPower(invalid_config, self.llm_service_manager)
        with self.assertRaises(ValueError) as context:
            brand_power._BrandPower__check_run_params()
        self.assertTrue(
            "Invalid target industries specified" in str(context.exception)
        )

    def test_get_list_competitors_prompt(self):
        """Test competitor list prompt generation"""
        prompt = self.brand_power._BrandPower__get_list_competitors_prompt()
        self.assertIsInstance(prompt, str)
        self.assertIn(self.base_config["company_name"], prompt)
        self.assertIn(self.base_config["company_website"], prompt)
        self.assertIn("Technology", prompt)  # Should contain the industry
        self.assertIn(self.base_config["location"], prompt)
        self.assertIn("competitor1", prompt)
        self.assertIn("competitor2", prompt)


    def test_configure_init_tasks(self):
        """Test initialization of pipeline tasks"""
        self.brand_power.configure_init_tasks()
        # Verify pre-validation tasks
        self.assertIn(
            "Check run params",
            self.brand_power._pre_validation_pipeline_tasks
        )
        # Verify extract tasks
        self.assertIn(
            "Get prompt data from LLM", self.brand_power._extract_pipeline_tasks
        )

    def tearDown(self):
        """Clean up temporary files after each test."""
        if os.path.exists(self.temp_cache_file):
            os.remove(self.temp_cache_file)
        os.rmdir(self.temp_dir)

    def test_cache_initialization(self):
        """Test that cache-related attributes are properly initialized"""
        self.assertEqual(self.brand_power._use_cache, True)  # Default value
        self.assertIsInstance(self.brand_power._llm_response_data, dict)
        self.assertEqual(self.brand_power._cache_file, "cache/brand_power.json")

    def test_cache_initialization_with_use_cache_false(self):
        """Test cache initialization when use_cache is set to False"""
        config_with_cache_false = self.base_config.copy()
        config_with_cache_false["use_cache"] = False
        brand_power = BrandPower(config_with_cache_false, self.llm_service_manager)
        self.assertEqual(brand_power._use_cache, False)

    @patch('os.makedirs')
    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_save_cache(self, mock_json_dump, mock_open, mock_makedirs):
        """Test cache saving functionality"""
        # Set up test data
        self.brand_power._llm_response_data = {"test": "data"}
        self.brand_power._cache_file = self.temp_cache_file
        
        # Call save_cache
        self.brand_power.save_cache()
        
        # Verify directory creation and file operations
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once()
        mock_json_dump.assert_called_once_with(
            {"test": "data"}, 
            mock_open.return_value.__enter__.return_value, 
            indent=2, 
            default=str
        )

    def test_load_cache_file_not_exists(self):
        """Test load_cache when cache file doesn't exist"""
        self.brand_power._cache_file = "nonexistent_file.json"
        result = self.brand_power.load_cache()
        self.assertFalse(result)

    def test_load_cache_use_cache_false(self):
        """Test load_cache when use_cache is False"""
        self.brand_power._use_cache = False
        # Create a cache file
        with open(self.temp_cache_file, 'w') as f:
            json.dump({"test": "data"}, f)
        self.brand_power._cache_file = self.temp_cache_file
        
        result = self.brand_power.load_cache()
        self.assertFalse(result)

    def test_load_cache_success(self):
        """Test successful cache loading"""
        # Create test cache data
        test_data = {"target_company": {"test": "data"}}
        with open(self.temp_cache_file, 'w') as f:
            json.dump(test_data, f)
        
        self.brand_power._cache_file = self.temp_cache_file
        result = self.brand_power.load_cache()
        
        self.assertTrue(result)
        self.assertEqual(self.brand_power._llm_response_data, test_data)

    def test_is_cached_with_use_cache_true(self):
        """Test is_cached when use_cache is True"""
        self.brand_power._use_cache = True
        self.brand_power._llm_response_data = {"test_key": "test_value"}
        
        self.assertTrue(self.brand_power.is_cached("test_key"))
        self.assertFalse(self.brand_power.is_cached("nonexistent_key"))

    def test_is_cached_with_use_cache_false(self):
        """Test is_cached when use_cache is False"""
        self.brand_power._use_cache = False
        self.brand_power._llm_response_data = {"test_key": "test_value"}
        
        self.assertFalse(self.brand_power.is_cached("test_key"))

    @patch('os.makedirs')
    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_save_cache_with_use_cache_false(self, mock_json_dump, mock_open, mock_makedirs):
        """Test that save_cache does nothing when use_cache is False"""
        self.brand_power._use_cache = False
        self.brand_power._llm_response_data = {"test": "data"}
        
        # Call save_cache
        self.brand_power.save_cache()
        
        # Verify no file operations occurred
        mock_makedirs.assert_not_called()
        mock_open.assert_not_called()
        mock_json_dump.assert_not_called()


class TestCompanyDataResponse(unittest.TestCase):
    def test_from_dict_complete_data(self):
        """Test CompanyDataResponse.from_dict with complete data"""
        test_dict = {
            "name": "Test Company",
            "competitors": ["Competitor 1", "Competitor 2"],
            "sources_from_pull": ["source1.com", "source2.com"]
        }
        
        response = CompanyDataResponse.from_dict(test_dict)
        
        self.assertEqual(response.name, "Test Company")
        self.assertEqual(response.competitors, ["Competitor 1", "Competitor 2"])
        self.assertEqual(response.sources_from_pull, ["source1.com", "source2.com"])

    def test_from_dict_missing_fields(self):
        """Test CompanyDataResponse.from_dict with missing fields"""
        test_dict = {"name": "Test Company"}
        
        response = CompanyDataResponse.from_dict(test_dict)
        
        self.assertEqual(response.name, "Test Company")
        self.assertEqual(response.competitors, [])
        self.assertEqual(response.sources_from_pull, [])

    def test_from_dict_empty_dict(self):
        """Test CompanyDataResponse.from_dict with empty dictionary"""
        response = CompanyDataResponse.from_dict({})
        
        self.assertEqual(response.name, "")
        self.assertEqual(response.competitors, [])
        self.assertEqual(response.sources_from_pull, [])


class TestCacheDataConversion(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.base_config = {
            "target_industries": ["Technology"],
            "company_name": "test_company",
            "description_of_company": "Test company description",
            "company_website": "www.testcompany.com",
            "location": "Test Location",
            "known_competitors": ["competitor1", "competitor2"]
        }
        self.llm_service_manager = Mock()
        self.brand_power = BrandPower(self.base_config, self.llm_service_manager)

    def test_convert_cached_data_to_objects_target_company(self):
        """Test conversion of cached target company data to objects"""
        # Set up test data with dictionary format (as it would be loaded from JSON)
        self.brand_power._llm_response_data = {
            "target_company": {
                "TestCorp": {
                    "company_data_response": {
                        "name": "TestCorp",
                        "competitors": ["Comp1", "Comp2"],
                        "sources_from_pull": ["source1.com"]
                    }
                }
            }
        }
        
        # Call the conversion method
        self.brand_power._convert_cached_data_to_objects()
        
        # Verify the data was converted to CompanyDataResponse object
        target_company_data = self.brand_power._llm_response_data["target_company"]["TestCorp"]["company_data_response"]
        self.assertIsInstance(target_company_data, CompanyDataResponse)
        self.assertEqual(target_company_data.name, "TestCorp")
        self.assertEqual(target_company_data.competitors, ["Comp1", "Comp2"])

    def test_convert_cached_data_to_objects_competitors(self):
        """Test conversion of cached competitor data to objects"""
        # Set up test data with dictionary format
        self.brand_power._llm_response_data = {
            "competitors": {
                "Competitor1": {
                    "company_data_response": {
                        "name": "Competitor1",
                        "competitors": ["Other1", "Other2"],
                        "sources_from_pull": ["comp1source.com"]
                    }
                }
            }
        }
        
        # Call the conversion method
        self.brand_power._convert_cached_data_to_objects()
        
        # Verify the data was converted to CompanyDataResponse object
        competitor_data = self.brand_power._llm_response_data["competitors"]["Competitor1"]["company_data_response"]
        self.assertIsInstance(competitor_data, CompanyDataResponse)
        self.assertEqual(competitor_data.name, "Competitor1")
        self.assertEqual(competitor_data.competitors, ["Other1", "Other2"])

    def test_convert_cached_data_already_objects(self):
        """Test conversion when data is already CompanyDataResponse objects"""
        # Set up test data with already converted objects
        response_obj = CompanyDataResponse(
            name="TestCorp",
            competitors=["Comp1"],
            sources_from_pull=["source1.com"]
        )
        self.brand_power._llm_response_data = {
            "target_company": {
                "TestCorp": {
                    "company_data_response": response_obj
                }
            }
        }
        
        # Call the conversion method
        self.brand_power._convert_cached_data_to_objects()
        
        # Verify the object remains unchanged
        target_company_data = self.brand_power._llm_response_data["target_company"]["TestCorp"]["company_data_response"]
        self.assertIsInstance(target_company_data, CompanyDataResponse)
        self.assertEqual(target_company_data.name, "TestCorp")


if __name__ == '__main__':
    unittest.main()
