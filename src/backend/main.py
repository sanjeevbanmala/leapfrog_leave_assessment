import os
import sys
import json
import requests

from flask import Flask, jsonify, request

from utils.constants import URL, DEFAULT_BEARER_TOKEN


app = Flask(__name__)


def get_leave_info(bearer_token=DEFAULT_BEARER_TOKEN):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({"error": "Unauthorized"}), 401


@app.route("/")
def index():
    return jsonify({"success": True})


@app.route("/leave_info", methods=["GET"])
def leave_info():
    auth_header = DEFAULT_BEARER_TOKEN or request.headers.get("Authorization")

    if auth_header:
        bearer_token = auth_header.replace("Bearer ", "", 1)
        response = get_leave_info(bearer_token)
        return response
    else:
        return jsonify({"error": "No Authorization header found"}), 401

if __name__ == "__main__":
    app.run()
