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

    # Example usage

    # Get access token
    access_token = tire_api.get_access_token()
    print("Access Token:", access_token)

    # Get vehicle list, tire list, sensor list, and tbox list
    vehicle_list = tire_api.get_vehicle_list()
    print("Vehicle List:", vehicle_list)

    tire_list = tire_api.get_tire_list()
    print("Tire List:", tire_list)

    sensor_list = tire_api.get_sensor_list()
    print("Sensor List:", sensor_list)

    tbox_list = tire_api.get_tboxes_list()
    print("Tbox List:", tbox_list)

    # Get vehicle info, tire info, and tires info by vehicle
    # Replace with actual vehicle and tire IDs from your data
    VEHICLE_ID = 7543
    vehicle_info = tire_api.get_vehicle_info(vehicle_id=VEHICLE_ID)
    print("Vehicle Info:", vehicle_info)

    tires_info = tire_api.get_tires_info_by_vehicle(vehicle_id=VEHICLE_ID)
    print("Tires Info by Vehicle:", tires_info)

    TIRE_ID = 47048
    tire_info = tire_api.get_tire_info(tire_id=TIRE_ID)
    print("Tire Info:", tire_info)

    # Get sensor info and tbox info
    # Replace with actual sensor and tbox IDs from your data
    SENSOR_ID = 48899
    sensor_info = tire_api.get_sensor_info(sensor_id=SENSOR_ID)
    print("Sensor Info:", sensor_info)

    TBOX_ID = 8694
    tbox_info = tire_api.get_tbox_info(tbox_id=TBOX_ID)
    print("Tbox Info:", tbox_info)

    # Get tire brands
    tire_brands = tire_api.get_tire_brands()
    print("Tire Brands:", tire_brands)

    # Get tire sizes
    tire_sizes = tire_api.get_tire_sizes()
    print("Tire Sizes:", tire_sizes)

    # Get vehicle models
    vehicle_models = tire_api.get_vehicle_models()
    print("Vehicle Models:", vehicle_models)

    # Get axle types
    axle_types = tire_api.get_axle_types()
    print("Axle Types:", axle_types)


    # Register a new vehicle
    new_vehicle = {
        "isTractor": 0,
        "licensePlateNumber": "ABC123",
        "emptyWeight": "1000",
        "fullWeight": "2000",
        "axleTypeId": "2",
        "modelId": "31",
        "orgId": "218",
    }

    #response = tire_api.add_vehicle(new_vehicle)
    #print("Add Vehicle Response:", response)

    # Update vehicle
    updated_vehicle = {
        "id": "7609",
        "isTractor": 0,
        "licensePlateNumber": "XYZ789",
        "emptyWeight": "1200",
        "fullWeight": "2200",
        "axleTypeId": "2",
        "modelId": "31",
        "orgId": "218",
    }

    response = tire_api.update_vehicle(updated_vehicle)
    print("Update Vehicle Response:", response)


