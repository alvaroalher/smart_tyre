"""Smart Tyre API Client
This module provides a client for interacting with the SmartTyre API.
"""

import json
import secrets
import time

import requests

from sign_util import SignUtil


class SmartTyreAPI:
    """
    A class to interact with the Smart Tyre API.
    """

    def __init__(self, base_url, client_id, client_secret, sign_key):
        """
        Initializes the SmartTyreAPI with the necessary credentials.

        Args:
            base_url (str): The base URL of the Smart Tyre API.
            client_id (str): The client ID for authentication.
            client_secret (str): The client secret for authentication.
            sign_key (str): The signing key used to generate the signature.
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.sign_key = sign_key

    def _new_header(self, need_access_token=True):
        if need_access_token:
            access_token = self.get_access_token()

            return {
                "clientId": self.client_id,
                "timestamp": str(int(time.time() * 1000)),
                "nonce": secrets.token_hex(16),
                "accessToken": access_token,
            }

        return {
            "clientId": self.client_id,
            "timestamp": str(int(time.time() * 1000)),
            "nonce": secrets.token_hex(16),
        }

    def _new_signature(self, headers, body, params, paths):
        return SignUtil.sign(
            headers=headers,
            body=body,
            params=params,
            paths=paths,
            sign_key=self.sign_key,
        )

    def _new_get_request(self, endpoint, params):
        url = f"{self.base_url}{endpoint}"
        headers = self._new_header()
        headers["sign"] = self._new_signature(headers, "", params, [])
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"

        response = requests.get(url, headers=headers, params=params, timeout=20)
        if response.status_code == 200:
            return response.json().get("data")
        return None

    def _new_post_request(
        self, endpoint, body, need_access_token=True, returns_data=True
    ):
        url = f"{self.base_url}{endpoint}"
        headers = self._new_header(need_access_token)
        headers["sign"] = self._new_signature(headers, body, {}, [])
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        response = requests.post(url, headers=headers, data=body, timeout=20)
        if response.status_code == 200 and returns_data:
            return response.json().get("data")
        if response.status_code == 200:
            return response.json().get("msg")
        return None

    def get_access_token(self):
        """
        Obtains an access token from the Smart Tyre API.

        Args:
            base_url (str): The base URL of the Smart Tyre API.
            client_id (str): The client ID for authentication.
            client_secret (str): The client secret for authentication.
            sign_key (str): The signing key used to generate the signature.

        Returns:
            The access token received from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/auth/oauth20/authorize"

        body = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "grantType": "client_credentials",
        }

        body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)

        response = self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            need_access_token=False,
        )

        return response.get("accessToken") if response else None

    # Vehicle Management

    def add_vehicle(self, vehicle_info):
        """
        Creates a new vehicle in the Smart Tyre system.
        Args:
            vehicle_info (dict): The information of the vehicle to be created.

                The dictionary should contain:

                - isTractor (int): 0 for non-tractor, 1 for tractor, 2 for trailer
                - licensePlateNumber (str): The license plate number of the vehicle
                - emptyWeight (str): The empty weight of the vehicle
                - fullWeight (str): The full weight of the vehicle
                - axleTypeId (str): The ID of the axle type
                - modelId (str): The ID of the vehicle model
                - orgId (str): The ID of the organization
                - tboxId (str): The ID of the TBox. Optional
                - vehicleChassisNumber (str): The chassis number of the vehicle. Optional

        Example:
            ```python
            new_vehicle = {
                "isTractor": 0,
                "licensePlateNumber": "ABC123",
                "emptyWeight": "1000",
                "fullWeight": "2000",
                "axleTypeId": "2",
                "modelId": "31",
                "orgId": "218"
            }
            ```

        Note: The vehicle_info dictionary must follow the API requirements.
        Check the API documentation for optional fields.

        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/vehicle/insert"

        body_str = json.dumps(vehicle_info, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def update_vehicle(self, vehicle_info):
        """
        Updates an existing vehicle in the Smart Tyre system.
        Args:
            vehicle_info (dict): The information of the vehicle to be updated.

                The dictionary should contain:

                - id (str): The ID of the vehicle to be updated
                - isTractor (int): 0 for non-tractor, 1 for tractor, 2 for trailer
                - licensePlateNumber (str): The license plate number of the vehicle
                - emptyWeight (str): The empty weight of the vehicle
                - fullWeight (str): The full weight of the vehicle
                - axleTypeId (str): The ID of the axle type
                - modelId (str): The ID of the vehicle model
                - orgId (str): The ID of the organization
                - tboxId (str): The ID of the TBox. Optional
                - vehicleChassisNumber (str): The chassis number of the vehicle. Optional


        Example:
             ```python
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
            ```
        Note: The vehicle_info dictionary must follow the API requirements.
        Check the API documentation for optional fields.

        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/vehicle/update"

        body_str = json.dumps(vehicle_info, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def get_vehicle_list(self):
        """
        Obtains the list of vehicles from the Smart Tyre API.

        Returns:
            The list of vehicles if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/vehicle/list"

        return self._new_get_request(endpoint, params={})

    def get_vehicle_info(self, vehicle_id):
        """
        Obtains detailed information about a specific vehicle.
        Args:
            vehicle_id (str): The ID of the vehicle.
        Returns:
            The detailed information about the vehicle if available or None if the request fails.
        """
        if not vehicle_id:
            return None

        endpoint = "/smartyre/openapi/vehicle/detail"

        params = {
            "vehicleId": [str(vehicle_id)],
        }

        return self._new_get_request(endpoint, params=params)

    # Tire Management

    def add_tire(self, tire_info):
        """
        Adds a new tire to the Smart Tyre system.
        Args:
            tire_info (dict): The information of the tire to be added.

                The dictionary should contain:
                - tyreCode (str): The identification code of the tire
                - tyreBrandId (str): The ID of the tire brand
                - tyreSizeId (str): The ID of the tire size
                - tyrePattern (str): The pattern of the tire
                - initialTreadDepth (str): The initial tread depth of the tire
                - orgId (str): The ID of the organization. Optional
                - sensorId (str): The ID of the sensor. Optional
                - totalDistance (str): The total distance of the tire (km). Optional
                - loadIndex (str): The load index of the tire. Optional
                - speedLevel (str): The speed level of the tire. Optional
                - newTreadDepth (str): The new tread depth of the tire. Optional

        Example:
            ```python
            new_tire = {
                "tyreCode": "ABC123",
                "tyreBrandId": "1",
                "tyreSizeId": "121",
                "tyrePattern": "Pattern A",
                "initialTreadDepth": "10"
            }
            ```

        Note: The tire_info dictionary must follow the API requirements.
        Check the API documentation for optional fields.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tyre/insert"

        body_str = json.dumps(tire_info, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def update_tire(self, tire_info):
        """
        Updates an existing tire in the Smart Tyre system.
        Args:
            tire_info (dict): The information of the tire to be updated.

                The dictionary should contain:
                - id (str): The ID of the tire to be updated
                - tyreCode (str): The identification code of the tire, this cannot be changed
                - tyreBrandId (str): The ID of the tire brand
                - tyreSizeId (str): The ID of the tire size
                - tyrePattern (str): The pattern of the tire
                - initialTreadDepth (str): The initial tread depth of the tire
                - orgId (str): The ID of the organization. Optional
                - sensorId (str): The ID of the sensor. Optional
                - totalDistance (str): The total distance of the tire (km). Optional
                - loadIndex (str): The load index of the tire. Optional
                - speedLevel (str): The speed level of the tire. Optional
                - newTreadDepth (str): The new tread depth of the tire. Optional
        Example:
            ```python
            updated_tire = {
                "id": "47414",
                "tyreCode": "ABC123",
                "tyreBrandId": "8",
                "tyreSizeId": "121",
                "tyrePattern": "Pattern B",
                "initialTreadDepth": "12"
            }
            ```
        Note: The tire_info dictionary must follow the API requirements.
        Check the API documentation for optional fields.

        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tyre/update"

        body_str = json.dumps(tire_info, separators=(",", ":"), ensure_ascii=False)
        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def get_tires_info_by_vehicle(self, vehicle_id):
        """
        Obtains tire information for a specific vehicle.
        Args:
            vehicle_id (str): The ID of the vehicle.
        Returns:
            The tire information if available or None if the request fails.
        """

        if not vehicle_id:
            return None

        endpoint = "/smartyre/openapi/vehicle/tyre/data"

        body_str = json.dumps({"vehicleId": vehicle_id}, separators=(",", ":"))

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
        )

    def get_tire_list(self):
        """Obtains the list of tires from the Smart Tyre API.
        Returns:
            The list of tires if available or None if the request fails.
        """

        endpoint = "/smartyre/openapi/tyre/list"

        return self._new_get_request(endpoint, params={})

    def get_tire_info(self, tire_id):
        """
        Obtains detailed information about a specific tire.
        Args:
            tire_id (str): The ID of the tire.
        Returns:
            The detailed information about the tire if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tyre/detail"
        params = {
            "id": [str(tire_id)],
        }
        return self._new_get_request(endpoint, params=params)

    def bind_tire_to_vehicle(self, vehicle_id, tire_code, axle_index, wheel_index):
        """
        Binds a tire to a vehicle in the Smart Tyre system.
        Args:
            vehicle_id (str): The ID of the vehicle.
            tire_code (str): The ID of the tire.
            axle_index (int): The index of the axle.
            wheel_index (int): The index of the wheel.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/vehicle/tyre/bind"

        body = {
            "vehicleId": vehicle_id,
            "tyreCode": tire_code,
            "axleIndex": axle_index,
            "wheelIndex": wheel_index,
        }

        body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def unbind_tire_from_vehicle(self, vehicle_id, tire_id):
        """
        Unbinds a tire from a vehicle in the Smart Tyre system.
        Args:
            vehicle_id (str): The ID of the vehicle.
            tire_id (str): The ID of the tire.
        Returns:
            The response from the API if available or None if the request fails.
        """

        endpoint = "/smartyre/openapi/vehicle/tyre/unbind"
        body = {
            "vehicleId": vehicle_id,
            "tyreCode": tire_id,
        }

        body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
        return self._new_post_request(
            endpoint=endpoint, body=body_str, returns_data=False
        )

    # Tbox Management

    def add_tbox(self, tbox_info):
        """
        Adds a new TBox to the Smart Tyre system.
        Args:
            tbox_info (dict): The information of the TBox to be added.

                The dictionary should contain:
                - tboxCode (str): The identification code of the TBox.
                    Must be 12 characters from 0-9 and A-F.
                - version (str): The version of the TBox. Optional
                - orgId (str): The ID of the organization. Optional
                - ioTCardNumber (str): The IoT card number of the TBox. Optional
                - carrier (str): The carrier of the TBox. Optional
                - remark (str): Additional remarks about the TBox. Optional

        Note: The tbox_info dictionary must follow the API requirements.
        Check the API documentation for optional fields.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tbox/insert"

        body_str = json.dumps(tbox_info, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def update_tbox(self, tbox_info):
        """
        Updates an existing TBox in the Smart Tyre system.
        Args:
            tbox_info (dict): The information of the TBox to be updated.

                The dictionary should contain:
                - id (str): The ID of the TBox to be updated.
                - tboxCode (str): The identification code of the Tbox to be updated.
                    Cannot be changed.
                - version (str): The version of the TBox. Optional
                - orgId (str): The ID of the organization. Optional
                - ioTCardNumber (str): The IoT card number of the TBox. Optional
                - carrier (str): The carrier of the TBox. Optional
                - remark (str): Additional remarks about the TBox. Optional

        Note: The tbox_info dictionary must follow the API requirements.
        Check the API documentation for optional fields.

        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tbox/update"

        body_str = json.dumps(tbox_info, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def get_tboxes_list(self):
        """
        Obtains the list of TBoxes from the Smart Tyre API.

        Returns:
            The list of TBoxes if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tbox/list"

        return self._new_get_request(endpoint, params={})

    def get_tbox_info(self, tbox_id):
        """
        Obtains information about a specific TBox.
        Args:
            tbox_id (str): The ID of the TBox.
        Returns:
            The detailed information about the TBox if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tbox/detail"
        params = {
            "id": [str(tbox_id)],
        }
        return self._new_get_request(endpoint, params=params)

    # Sensor Management

    def add_sensor(self, sensor_info):
        """
        Adds a new sensor to the Smart Tyre system.
        Args:
            sensor_info (dict): The information of the sensor to be added.

                The dictionary should contain:
                - sensorCode (str): The identification code of the sensor.
                    Must be 12 characters from 0-9 and A-F.
                - version (str): The version of the sensor. Optional
                - orgId (str): The ID of the organization. Optional
                - remark (str): Additional remarks about the sensor. Optional

        Note: The sensor_info dictionary must follow the API requirements.
        Check the API documentation for optional fields.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/sensor/insert"

        body_str = json.dumps(sensor_info, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def update_sensor(self, sensor_info):
        """
        Updates an existing sensor in the Smart Tyre system.
        Args:
            sensor_info (dict): The information of the sensor to be updated.

                The dictionary should contain:
                - id (str): The ID of the sensor to be updated.
                - sensorCode (str): The identification code of the sensor.
                    Must be 12 characters from 0-9 and A-F.
                - version (str): The version of the sensor. Optional
                - orgId (str): The ID of the organization. Optional
                - remark (str): Additional remarks about the sensor. Optional

        Note: The sensor_info dictionary must follow the API requirements.
        Check the API documentation for optional fields.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/sensor/update"

        body_str = json.dumps(sensor_info, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def get_sensor_list(self):
        """
        Obtains the list of sensors from the Smart Tyre API.
        Returns:
            The list of sensors if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/sensor/list"

        return self._new_get_request(endpoint, params={})

    def get_sensor_info(self, sensor_id):
        """
        Obtains information about a specific sensor.
        Args:
            sensor_id (str): The ID of the sensor.
        Returns:
            The detailed information about the sensor if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/sensor/detail"
        params = {
            "id": [str(sensor_id)],
        }
        return self._new_get_request(endpoint, params=params)

    def bind_sensor_to_tire(self, tire_code, vehicle_id, axle_index, wheel_index, sensor_code):
        """
        Binds a sensor to a tire in the Smart Tyre system.
        Args:
            tire_code (str): The ID of the tire.
            vehicle_id (str): The ID of the vehicle.
            axle_index (int): The index of the axle.
            wheel_index (int): The index of the wheel.
            sensor_code (str): The ID of the sensor.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tyre/sensor/bind"

        body = {
            "tyreCode": tire_code,
            "vehicleId": vehicle_id,
            "axleIndex": axle_index,
            "wheelIndex": wheel_index,
            "sensorCode": sensor_code,
        }

        body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    def unbind_sensor_from_tire(self, tire_code, vehicle_id, axle_index, wheel_index, sensor_code):
        """
        Unbinds a sensor from a tire in the Smart Tyre system.
        Args:
            tire_code (str): The ID of the tire.
            vehicle_id (str): The ID of the vehicle.
            axle_index (int): The index of the axle.
            wheel_index (int): The index of the wheel.
            sensor_code (str): The ID of the sensor.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tyre/sensor/unbind"

        body = {
            "tyreCode": tire_code,
            "vehicleId": vehicle_id,
            "axleIndex": axle_index,
            "wheelIndex": wheel_index,
            "sensorCode": sensor_code,
        }

        body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False,
        )

    # Reference Data Management
    def get_tire_brands(self):
        """
        Obtains the list of tire brands from the Smart Tyre API.
        Returns:
            The list of tire brands if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tyre/brand/all"

        return self._new_get_request(endpoint, params={})

    def get_tire_sizes(self):
        """
        Obtains the list of tire sizes from the Smart Tyre API.
        Returns:
            The list of tire sizes if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/tyre/size/all"

        return self._new_get_request(endpoint, params={})

    def get_vehicle_models(self):
        """
        Obtains the list of vehicle models from the Smart Tyre API.
        Returns:
            The list of vehicle models if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/vehicle/model/all"

        return self._new_get_request(endpoint, params={})

    def get_axle_types(self):
        """
        Obtains the list of axle types from the Smart Tyre API.
        Returns:
            The list of axle types if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/vehicle/axle/all"

        return self._new_get_request(endpoint, params={})
