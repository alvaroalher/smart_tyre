"""SmartTyre API Client
This module provides a client for interacting with the SmartTyre API."""

import os

from dotenv import load_dotenv

from smarttyre_api import SmartTyreAPI

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SIGN_KEY = os.getenv("SIGN_KEY")


def menu():
    """Display the menu options."""
    print("1. Get Access Token")
    print("2. Get Vehicle List")
    print("3. Get Vehicle Info")
    print("4. Get Tire List")
    print("5. Get Tires Info by Vehicle")
    print("6. Get Tire Info")
    print("7. Get Sensor Info")
    print("8. Get Tbox Info")
    print("9. Get Tire Brands")
    print("10. Get Tire Sizes")
    print("11. Get Vehicle Models")
    print("12. Get Axle Types")
    print("13. Add Vehicle")
    print("14. Update Vehicle")
    print("15. Add Tire")
    print("16. Update Tire")
    print("17. Add Sensor")
    print("18. Update Sensor")
    print("19. Add Tbox")
    print("20. Update Tbox")
    print("21. Get Tbox List")
    print("22. Get Sensor List")
    print("23. Bind Tire")
    print("24. Unbind Tire")
    print("25. Bind Sensor")
    print("26. Unbind Sensor")
    print("25. Exit")
    print("Please select an option (1-25): ", end="")


if __name__ == "__main__":
    tire_api = SmartTyreAPI(
        base_url="https://www.dajintruck.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        sign_key=SIGN_KEY,
    )

    menu()
    choice = input("Option: ")
    if choice == "1":  # Get access token
        access_token = tire_api.get_access_token()
        print("Access Token:", access_token)
    elif choice == "2":  # Get vehicle list
        vehicle_list = tire_api.get_vehicle_list()
        print("Vehicle List:", vehicle_list)
    elif choice == "3":  # Get vehicle info
        vehicle_id = input("Enter Vehicle ID: ")
        vehicle_info = tire_api.get_vehicle_info(vehicle_id=vehicle_id)
        print("Vehicle Info:", vehicle_info)
    elif choice == "4":  # Get tire list
        tire_list = tire_api.get_tire_list()
        print("Tire List:", tire_list)
    elif choice == "5":  # Get tires info by vehicle
        vehicle_id = input("Enter Vehicle ID: ")
        tires_info = tire_api.get_tires_info_by_vehicle(vehicle_id=vehicle_id)
        print("Tires Info by Vehicle:", tires_info)
    elif choice == "6":  # Get tire info
        tire_id = input("Enter Tire ID: ")
        tire_info = tire_api.get_tire_info(tire_id=tire_id)
        print("Tire Info:", tire_info)
    elif choice == "7":  # Get sensor info
        sensor_id = input("Enter Sensor ID: ")
        sensor_info = tire_api.get_sensor_info(sensor_id=sensor_id)
        print("Sensor Info:", sensor_info)
    elif choice == "8":  # Get tbox info
        tbox_id = input("Enter Tbox ID: ")
        tbox_info = tire_api.get_tbox_info(tbox_id=tbox_id)
        print("Tbox Info:", tbox_info)
    elif choice == "9":  # Get tire brands
        tire_brands = tire_api.get_tire_brands()
        print("Tire Brands:", tire_brands)
    elif choice == "10":  # Get tire sizes
        tire_sizes = tire_api.get_tire_sizes()
        print("Tire Sizes:", tire_sizes)
    elif choice == "11":  # Get vehicle models
        vehicle_models = tire_api.get_vehicle_models()
        print("Vehicle Models:", vehicle_models)
    elif choice == "12":  # Get axle types
        axle_types = tire_api.get_axle_types()
        print("Axle Types:", axle_types)
    elif choice == "13":  # Add vehicle
        new_vehicle = {
            "isTractor": 0,
            "licensePlateNumber": "ABC123",
            "emptyWeight": "1000",
            "fullWeight": "2000",
            "axleTypeId": "2",
            "modelId": "31",
            "orgId": "218",
        }
        response = tire_api.add_vehicle(new_vehicle)
        print("Add Vehicle Response:", response)
    elif choice == "14":  # Update vehicle
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
    elif choice == "15":  # Add tire
        new_tire = {
            "tyreCode": "ABC123",
            "tyreBrandId": "1",
            "tyreSizeId": "121",
            "tyrePattern": "Pattern A",
            "initialTreadDepth": "10",
        }
        response = tire_api.add_tire(new_tire)
        print("Add Tire Response:", response)
    elif choice == "16":  # Update tire
        updated_tire = {
            "id": "47414",
            "tyreCode": "ABC123",
            "tyreBrandId": "8",
            "tyreSizeId": "121",
            "tyrePattern": "Pattern B",
            "initialTreadDepth": "12",
        }
        response = tire_api.update_tire(updated_tire)
        print("Update Tire Response:", response)
    elif choice == "17":  # Add sensor
        new_sensor = {
            "sensorCode": "A4C1386C7403",
            "version": "2.5.0",
        }
        response = tire_api.add_sensor(new_sensor)
        print("Add Sensor Response:", response)
    elif choice == "18":  # Update sensor
        updated_sensor = {
            "id": "49356",
            "sensorCode": "A4C1386C7403",
            "version": "2.5.0",
            "orgId": "218",
            "remark": "sensor updated",
        }
        response = tire_api.update_sensor(updated_sensor)
        print("Update Sensor Response:", response)
    elif choice == "19":  # Add Tbox
        new_tbox = {
            "tboxCode": "A9C1386C7403",
        }
        response = tire_api.add_tbox(new_tbox)
        print("Add Tbox Response:", response)
    elif choice == "20":  # Update Tbox
        updated_tbox = {
            "id": "8756",
            "tboxCode": "A9C1386C7403",
            "version": "1.0",
        }
        response = tire_api.update_tbox(updated_tbox)
        print("Update Tbox Response:", response)
    elif choice == "21":  # Get Tbox List
        tbox_list = tire_api.get_tboxes_list()
        print("Tbox List:", tbox_list)
    elif choice == "22":  # Get Sensor List
        sensor_list = tire_api.get_sensor_list()
        print("Sensor List:", sensor_list)
    elif choice == "23":  # Bind tire to vehicle
        vehicle_id = input("Enter Vehicle ID: ")
        tire_id = input("Enter Tire ID: ")
        axle_idx = input("Enter Axle Index: ")
        wheel_id = input("Enter Wheel ID: ")
        response = tire_api.bind_tire_to_vehicle(
            vehicle_id, tire_id, axle_idx, wheel_id
        )
        print("Bind Tire Response:", response)
    elif choice == "24":  # Unbind tire from vehicle
        vehicle_id = input("Enter Vehicle ID: ")
        tire_id = input("Enter Tire ID: ")
        response = tire_api.unbind_tire_from_vehicle(vehicle_id, tire_id)
        print("Unbind Tire Response:", response)
    elif choice == "25":  # Bind sensor to tire
        tire_code = input("Enter Tire Code: ")
        sensor_code = input("Enter Sensor Code: ")
        vehicle_id = input("Enter Vehicle ID: ")
        axle_idx = input("Enter Axle Index: ")
        wheel_idx = input("Enter Wheel Index: ")
        response = tire_api.bind_sensor_to_tire(
            tire_code, vehicle_id, axle_idx, wheel_idx, sensor_code
        )
        print("Bind Sensor Response:", response)
    elif choice == "26":  # Unbind sensor from tire
        tire_code = input("Enter Tire Code: ")
        sensor_code = input("Enter Sensor Code: ")
        vehicle_id = input("Enter Vehicle ID: ")
        axle_idx = input("Enter Axle Index: ")
        wheel_idx = input("Enter Wheel Index: ")
        response = tire_api.unbind_sensor_from_tire(
            tire_code, vehicle_id, axle_idx, wheel_idx, sensor_code
        )
        print("Unbind Sensor Response:", response)
    else:
        print("Exiting...")
