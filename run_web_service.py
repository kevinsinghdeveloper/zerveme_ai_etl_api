from flask import Flask, request, jsonify

from controllers.auth.AuthenticationController import AuthenticationController
from controllers.report_processor.ReportProcessorController import ReportProcessorController
from handler.register_components import register_controller
from managers.auth.AuthenticationResourceManager import AuthenticationResourceManager
from managers.reports_processor.ReportProcessorResourceManager import ReportProcessorResourceManager
from utility.Utility import Utility
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api_config = Utility.read_in_json_file("configs/serp_config.json")
# ml_config = Utility.read_in_json_file("configs/ml_config.json")

# setup managers
report_processor_resource_manager = ReportProcessorResourceManager()
auth_resource_manager = AuthenticationResourceManager()

# register controllers
register_controller(app, ReportProcessorController, report_processor_resource_manager)
register_controller(app, AuthenticationController, auth_resource_manager)


def run_web_service():
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    run_web_service()

# TODO
#   add finishing pieces to rec -> we should manager a model, which will become a table
