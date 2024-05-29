import os

from dotenv import load_dotenv

load_dotenv()


# Constants
URL = "https://qa.vyaguta.lftechnology.com.np/api/leave/leaves?fetchType=all&startDate=2021-07-17&endDate=2024-04-23&size=10000&roleType=issuer"
DEFAULT_BEARER_TOKEN = os.getenv("BEARER_TOKEN", "")
