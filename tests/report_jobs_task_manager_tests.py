import unittest
from unittest.mock import Mock, patch
from managers.ReportJobsTaskManager import ReportJobTaskManager
from models.request.ReportProcessorRequestResourceModel import (
    ReportProcessorRequestResourceModel
)
from abstractions.enumerations.JobStatusEnum import JobStatusEnum


class TestReportJobTaskManager(unittest.TestCase):
    def setUp(self):
        self.etl_config = {"dummy": "config"}
        self.manager = ReportJobTaskManager(self.etl_config)
        self.default_task_type = JobStatusEnum.START
        self.default_report_name = "brand_power"
        self.default_task_params = {"param": "value"}
        self.default_llm_config = {"llm": "config"}

    def test_configure_sets_llm_manager(self):
        mock_llm_manager = Mock()
        self.manager.configure(llm_manager=mock_llm_manager)
        self.assertEqual(
            self.manager._ReportJobTaskManager__llm_manager, mock_llm_manager
        )

    @patch(
        'managers.ReportJobsTaskManager.ReportJobTaskManager'
        '._ReportJobTaskManager__get_report_instance'
    )
    def test_run_task_success(self, mock_get_report_instance):
        mock_etl_report = Mock()
        mock_get_report_instance.return_value = mock_etl_report
        mock_etl_report.run_etl.return_value = None
        request = ReportProcessorRequestResourceModel(
            task_type=self.default_task_type,
            report_name=self.default_report_name,
            task_params=self.default_task_params,
            llm_config=self.default_llm_config
        )
        self.manager._ReportJobTaskManager__llm_manager = Mock()
        result = self.manager.run_task(request)
        self.assertEqual(result["status"], "success")
        self.assertIn("Report run completed", result["message"])
        mock_etl_report.run_etl.assert_called_once()

    @patch(
        'managers.ReportJobsTaskManager.ReportJobTaskManager'
        '._ReportJobTaskManager__get_report_instance'
    )
    def test_run_task_unsupported_type(self, mock_get_report_instance):
        mock_etl_report = Mock()
        mock_get_report_instance.return_value = mock_etl_report
        request = ReportProcessorRequestResourceModel(
            task_type="INVALID",
            report_name=self.default_report_name,
            task_params=self.default_task_params,
            llm_config=self.default_llm_config
        )
        self.manager._ReportJobTaskManager__llm_manager = Mock()
        with self.assertRaises(ValueError):
            self.manager.run_task(request)

    @patch(
        'managers.ReportJobsTaskManager.ReportJobTaskManager'
        '._ReportJobTaskManager__get_report_instance'
    )
    def test_run_task_no_etl_report(self, mock_get_report_instance):
        mock_get_report_instance.return_value = None
        request = ReportProcessorRequestResourceModel(
            task_type=self.default_task_type,
            report_name=self.default_report_name,
            task_params=self.default_task_params,
            llm_config=self.default_llm_config
        )
        self.manager._ReportJobTaskManager__llm_manager = Mock()
        with self.assertRaises(Exception):
            self.manager.run_task(request)


if __name__ == '__main__':
    unittest.main()
