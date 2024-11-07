from flask import Flask, request, jsonify

from controllers.rec.RecSysController import RecSysController
from managers.SerpServiceManager import SerpServiceManager
from managers.rec.RecSysResourceManager import RecSysResourceManager
from utility.Utility import Utility

app = Flask(__name__)

api_config = Utility.read_in_json_file("configs/serp_config.json")
# setup services and controllers
serp_api_manager = SerpServiceManager(api_config=api_config)

rec_sys_resource_manager = RecSysResourceManager(serp_api_manager)

rec_sys_controller = RecSysController(app, rec_sys_resource_manager)


def run_web_service():
    app.run(host='0.0.0.0', port=1234)


if __name__ == '__main__':
    run_web_service()
