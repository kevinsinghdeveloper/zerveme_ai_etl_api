import unittest
from unittest.mock import Mock, patch
from report_etls.brand_power import BrandPower


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

    @patch('logging.info')
    def test_generate_base_prompts_logs_and_sets_prompt_data(
            self, mock_logging
    ):
        self.brand_power._BrandPower__generate_base_prompts()
        mock_logging.assert_called_with("Crafting prompts...")
        # Check prompt_data structure
        prompt_data = self.brand_power._prompt_data
        self.assertIn('list_competitors', prompt_data)
        self.assertIn('source_ranking', prompt_data)
        self.assertIn('system', prompt_data['list_competitors'])
        self.assertIn('user', prompt_data['list_competitors'])
        self.assertIn('system', prompt_data['source_ranking'])
        self.assertIn('user', prompt_data['source_ranking'])

    @patch('logging.info')
    @patch('logging.debug')
    def test_send_prompts_to_llm(self, mock_debug, mock_info):
        # Prepare prompt data
        self.brand_power._BrandPower__generate_base_prompts()
        # Mock LLM service manager and response
        mock_response = Mock()
        mock_response.response_content = '{"result": "ok"}'
        mock_response.history_messages = ["history"]
        self.brand_power._llm_service_manager.run_task.return_value = (
            mock_response
        )
        # Call send prompts
        self.brand_power._BrandPower__send_prompts_to_llm()
        self.brand_power._llm_service_manager.run_task.assert_called()
        mock_info.assert_any_call("Sending prompts to LLM...")
        mock_info.assert_any_call("List competitors response received.")
        mock_debug.assert_called()

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
            "Generate prompts", self.brand_power._extract_pipeline_tasks
        )
        self.assertIn(
            "Send prompts to LLM", self.brand_power._extract_pipeline_tasks
        )



if __name__ == '__main__':
    unittest.main()
