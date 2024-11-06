from flask import Flask, request, jsonify

app = Flask(__name__)

# setup services and controllers


def run_web_service():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    run_web_service()
