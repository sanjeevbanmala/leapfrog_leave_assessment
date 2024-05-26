import os
import sys
import json
import requests

from flask import Flask, jsonify, request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.util.constants import URL, DEFAULT_BEARER_TOKEN
from utils.database import connect_db, close_db
from utils.logging import get_logger

logger = get_logger()


app = Flask(__name__)


def get_leave_info(bearer_token=DEFAULT_BEARER_TOKEN):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        logger.info("Leave information successfully retrieved")
        return response.json()
    else:
        logger.error(
            "Failed to retrieve leave information. Status code: %d",
            response.status_code,
        )
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


@app.route("/insert_leave_info", methods=["GET"])
def insert_data():
    try:
        conn = connect_db()
        cur = conn.cursor()

        json_data = get_leave_info()

        # Extract data from json_data and insert into database
        data = json_data["data"]

        cur.execute("TRUNCATE TABLE raw.imported_leave_information")

        # insert query
        query = """
        INSERT INTO raw.imported_leave_information(
            id, userId, empId, teamManagerId, designationId, designationName, firstName, middleName, lastName, email, 
            isHr, isSupervisor, allocations, leaveIssuerId, currentLeaveIssuerId, leaveIssuerFirstName, leaveIssuerLastName, 
            currentLeaveIssuerEmail, departmentDescription, startDate, endDate, leaveDays, reason, status, remarks, leaveTypeId, 
            leaveTypeName, defaultDays, transferableDays, isConsecutive, fiscalId, fiscalStartDate, fiscalEndDate, fiscalIsCurrent, 
            createdAt, updatedAt, isConverted
        ) VALUES (
            %(id)s, %(userId)s, %(empId)s, %(teamManagerId)s, %(designationId)s, %(designationName)s, %(firstName)s, %(middleName)s, 
            %(lastName)s, %(email)s, %(isHr)s, %(isSupervisor)s, %(allocations)s, %(leaveIssuerId)s, %(currentLeaveIssuerId)s, 
            %(leaveIssuerFirstName)s, %(leaveIssuerLastName)s, %(currentLeaveIssuerEmail)s, %(departmentDescription)s, %(startDate)s, 
            %(endDate)s, %(leaveDays)s, %(reason)s, %(status)s, %(remarks)s, %(leaveTypeId)s, %(leaveTypeName)s, %(defaultDays)s, 
            %(transferableDays)s, %(isConsecutive)s, %(fiscalId)s, %(fiscalStartDate)s, %(fiscalEndDate)s, %(fiscalIsCurrent)s, 
            %(createdAt)s, %(updatedAt)s, %(isConverted)s
        )
        """

        for row in data:
            # Convert allocations to a JSON string if it's not None
            if row["allocations"] is not None:
                row["allocations"] = json.dumps(row["allocations"])
            cur.execute(query, row)
            conn.commit()

        # run procedures
        with open("../database/procedures.json") as f:
            proc_steps = json.load(f)

        # call each procedure in order
        for step in proc_steps["steps"]:
            cur.execute(f'CALL {step["proc"]}();')
            conn.commit()

        close_db(conn, cur)
        return jsonify({"success": "Leave Data Inserted Successfully!"})
        logger.info("Leave Data Inserted Successfully!")

    except Exception as e:
        conn.rollback()
        close_db(conn, cur)
        return jsonify({"error": f"Couldn't insert the leave data!{e}"})
        logger.error(f"Couldn't insert the leave data!{e}")


if __name__ == "__main__":
    app.run(debug=True)
