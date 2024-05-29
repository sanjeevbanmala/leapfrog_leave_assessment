import os
import sys
import json
import requests
import httpx
import asyncpg
import asyncio

from fastapi import FastAPI, HTTPException, Header
from util.constants import URL, DEFAULT_BEARER_TOKEN

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.database import connect_db, close_db
from utils.logging import get_logger
from util.sql_queries import insert_query

logger = get_logger()

app = FastAPI()


async def get_leave_info(bearer_token=DEFAULT_BEARER_TOKEN):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        response = await client.get(URL, headers=headers)
        if response.status_code == 200:
            logger.info("Leave information successfully retrieved")
            return response.json()
        else:
            logger.error(
                "Failed to retrieve leave information. Status code: %d",
                response.status_code,
            )
            raise HTTPException(status_code=401, detail="Unauthorized")


async def insert_leave_data(data, conn):
    async with conn.transaction():

        await conn.execute("TRUNCATE TABLE raw.imported_leave_information;")
        for row in data:
            # Convert allocations to a JSON string if it's not None
            if row["allocations"] is not None:
                row["allocations"] = json.dumps(row["allocations"])
            # Insert each row using the insert_query
            await conn.execute(insert_query, *row.values())


async def run_insert_leave_info():
    try:
        conn = await connect_db()

        json_data = await get_leave_info()

        # Extract data from json_data
        data = json_data["data"]

        # Insert data into database
        await insert_leave_data(data, conn)

        # run procedures
        with open("../db/procedures.json") as f:
            proc_steps = json.load(f)

        # call each procedure in order
        async with conn.transaction():
            for step in proc_steps["steps"]:
                await conn.execute(f'CALL {step["proc"]}();')

        await conn.close()
        logger.info("Leave Data Inserted Successfully!")
        return {"success": "Leave Data Inserted Successfully!"}

    except Exception as e:
        logger.error(f"Couldn't insert the leave data! {e}")
        raise HTTPException(
            status_code=500, detail=f"Couldn't insert the leave data! {e}"
        )


async def background_task():
    while True:
        await run_insert_leave_info()
        await asyncio.sleep(10)  # Sleep for 60 seconds


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_task())


@app.get("/")
async def index():
    return {"success": True}


@app.get("/leave_info")
async def leave_info(authorization: str = DEFAULT_BEARER_TOKEN):
    try:
        bearer_token = authorization.replace("Bearer ", "", 1)
        return await get_leave_info(bearer_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/insert_leave_info")
async def insert_data():
    try:
        return await run_insert_leave_info()
    except HTTPException as e:
        return {"error": e.detail}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
