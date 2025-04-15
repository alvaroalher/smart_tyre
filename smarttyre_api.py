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

    def _new_post_request(self, endpoint, body, need_access_token=True, returns_data=True):
        url = f"{self.base_url}{endpoint}"
        headers = self._new_header(need_access_token)
        headers["sign"] = self._new_signature(headers, body, {}, [])
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        response = requests.post(url, headers=headers, data=body, timeout=20)
        if response.status_code == 200 and returns_data:
            return response.json().get("data")
        if response.status_code == 200:
            return response.json().get("message")
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
        """Obtain the list of tires from the Smart Tyre API.
        Returns:
            The list of tires if available or None if the request fails.
        """

        endpoint = "/smartyre/openapi/tyre/list"

        return self._new_get_request(endpoint, params={})

    def create_vehicle(self, vehicle_info):
        """
        Create a new vehicle in the Smart Tyre system.
        Args:
            vehicle_info (dict): The information of the vehicle to be created.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/vehicle/insert"

        body_str = json.dumps(vehicle_info, separators=(",", ":"), ensure_ascii=False)

        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
        )

    def update_vehicle(self, vehicle_info):
        """
        Update an existing vehicle in the Smart Tyre system.
        Args:
            vehicle_info (dict): The information of the vehicle to be updated.
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

    def bind_tire_to_vehicle(self, vehicle_id, tire_id, axle_index, wheel_index):
        """
        Bind a tire to a vehicle in the Smart Tyre system.
        Args:
            vehicle_id (str): The ID of the vehicle.
            tire_id (str): The ID of the tire.
            axle_index (int): The index of the axle.
            wheel_index (int): The index of the wheel.
        Returns:
            The response from the API if available or None if the request fails.
        """
        endpoint = "/smartyre/openapi/vehicle/tyre/bind"

        body = {
            "vehicleId": vehicle_id,
            "tyreId": tire_id,
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
        Unbind a tire from a vehicle in the Smart Tyre system.
        Args:
            vehicle_id (str): The ID of the vehicle.
            tire_id (str): The ID of the tire.
        Returns:
            The response from the API if available or None if the request fails.
        """

        endpoint = "/smartyre/openapi/vehicle/tyre/unbind"
        body = {
            "vehicleId": vehicle_id,
            "tyreId": tire_id,
        }

        body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
        return self._new_post_request(
            endpoint=endpoint,
            body=body_str,
            returns_data=False
        )
