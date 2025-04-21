"""SmartTyre API Client
This module provides a client for interacting with the SmartTyre API."""
import os

from dotenv import load_dotenv

from smarttyre_api import SmartTyreAPI

load_dotenv()

CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
SIGN_KEY=os.getenv("SIGN_KEY")

if __name__ == "__main__":
    tire_api = SmartTyreAPI(
        base_url="https://www.dajintruck.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        sign_key=SIGN_KEY,
    )

    #print(tire_api.get_access_token())
    #print(tire_api.get_vehicle_list())
    #print(tire_api.get_vehicle_info(7543))
    print(tire_api.get_sensor_list())
