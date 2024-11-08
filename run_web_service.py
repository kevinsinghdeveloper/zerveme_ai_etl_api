from flask import Flask, request, jsonify

from controllers.auth.AuthenticationController import AuthenticationController
from controllers.rec.RecSysController import RecSysController
from handler.register_components import register_controller
from managers.SerpServiceManager import SerpServiceManager
from managers.auth.AuthenticationResourceManager import AuthenticationResourceManager
from managers.rec.RecSysResourceManager import RecSysResourceManager
from utility.Utility import Utility

app = Flask(__name__)

api_config = Utility.read_in_json_file("configs/serp_config.json")

# setup services and controllers
serp_api_manager = SerpServiceManager(api_config=api_config)

rec_sys_resource_manager = RecSysResourceManager(serp_api_manager)
auth_resource_manager = AuthenticationResourceManager()

# register controllers
register_controller(app, RecSysController, rec_sys_resource_manager)
register_controller(app, AuthenticationController, auth_resource_manager)


def run_web_service():
    app.run(host='0.0.0.0', port=1234)


if __name__ == '__main__':
    run_web_service()

# TODO
#   fix interfaces, not strict as c#
#   setup and complete resource manager with request to serp
#   add finishing pieces to rec -> we should manager a model, which will become a table
