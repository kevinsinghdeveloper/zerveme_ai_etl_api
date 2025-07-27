import unittest
from unittest.mock import Mock, patch
from managers.reports_processor.ReportProcessorResourceManager import ReportProcessorResourceManager
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel


class TestReportProcessorResourceManager(unittest.TestCase):
    def setUp(self):
        self.mock_web_service_managers = {"etl_service_manager": Mock()}
        self.manager = ReportProcessorResourceManager(
            web_service_managers=self.mock_web_service_managers
        )
        self.request_model = Mock(spec=ReportProcessorRequestResourceModel)
        self.request_model.llm_config = {"llm": "config"}  # Ensure llm_config attribute exists

    @patch('managers.reports_processor.ReportProcessorResourceManager.jsonify')
    def test_get_returns_json(self, mock_jsonify):
        mock_jsonify.return_value = {"message": "Getting status", "data": []}
        result = self.manager.get(self.request_model)
        mock_jsonify.assert_called_once()
        self.assertEqual(result["message"], "Getting status")

    @patch('managers.reports_processor.ReportProcessorResourceManager.AIServiceHandler.get_ai_service')
    @patch('managers.reports_processor.ReportProcessorResourceManager.jsonify')
    def test_post_runs_task_and_returns_json(self, mock_jsonify, mock_get_ai_service):
        mock_llm_manager = Mock()
        mock_get_ai_service.return_value = mock_llm_manager
        mock_etl_service_manager = self.mock_web_service_managers["etl_service_manager"]
        mock_etl_service_manager.run_task.return_value = {"status": "success"}
        mock_jsonify.return_value = {"message": "Post request on task", "data": []}
        # Ensure llm_config attribute exists on request_model
        self.request_model.llm_config = {"llm": "config"}
        result = self.manager.post(self.request_model)
        mock_get_ai_service.assert_called_once_with(self.request_model.llm_config)
        mock_etl_service_manager.run_task.assert_called_once_with(self.request_model)
        mock_jsonify.assert_called_once()
        self.assertEqual(result["message"], "Post request on task")


if __name__ == '__main__':
    unittest.main() 