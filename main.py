"""SmartTyre API Client
This module provides a client for interacting with the SmartTyre API."""

from smarttyre_api import SmartTyreAPI

CLIENT_ID = "0a8e40fa33434d8a9faa62cccf9db037"
CLIENT_SECRET = "Fb3MvwsNcQjSPpRtqgpckOIf"
SIGN_KEY = "Za9rVu0WOoTxisRq"


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
    print(tire_api.get_tires_info_by_vehicle(7543))
