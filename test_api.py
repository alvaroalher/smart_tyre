"""Test the SmartTyreAPI class."""
import os

from dotenv import load_dotenv

from smarttyre_api import SmartTyreAPI

load_dotenv()


class TestAPI:
    def setup_method(self):
        self.api = SmartTyreAPI(
            base_url="https://www.dajintruck.com",
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            sign_key=os.getenv("SIGN_KEY"),
        )

    def test_get_access_token(self):
        token = self.api.get_access_token()
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_get_vehicle_list(self):
        vehicles = self.api.get_vehicle_list()
        assert vehicles is not None
        assert isinstance(vehicles, dict)
        assert len(vehicles) > 0

    def test_get_vehicle_info(self):
        vehicle_id = 7543
        vehicle_info = self.api.get_vehicle_info(vehicle_id)
        assert vehicle_info is not None
        assert isinstance(vehicle_info, dict)
        assert vehicle_info.get("id") == vehicle_id

    def test_get_tire_list(self):
        tires = self.api.get_tire_list()
        assert tires is not None
        assert isinstance(tires, dict)
        assert len(tires) > 0

    def test_get_tires_info_by_vehicle(self):
        vehicle_id = 7543
        tires_info = self.api.get_tires_info_by_vehicle(vehicle_id)
        assert tires_info is not None
        assert isinstance(tires_info, dict)
        assert len(tires_info) > 0

    def test_get_tires_info_by_vehicle_invalid_id(self):
        vehicle_id = 999999
        tires_info = self.api.get_tires_info_by_vehicle(vehicle_id)
        assert tires_info is None

    def test_get_tbox_list(self):
        tbox_list = self.api.get_tboxes_list()
        assert tbox_list is not None
        assert isinstance(tbox_list, dict)
        assert len(tbox_list) > 0

    def test_get_sensor_list(self):
        sensors = self.api.get_sensor_list()
        assert sensors is not None
        assert isinstance(sensors, dict)
        assert len(sensors) > 0
