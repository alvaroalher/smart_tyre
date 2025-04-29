"""Test the SmartTyreAPI class."""

import os

from dotenv import load_dotenv

from smarttyre_api import SmartTyreAPI

load_dotenv()


class TestAPI:
    def setup_method(self):
        """Set up the test environment by loading environment
        variables and initializing the API client."""
        self.api = SmartTyreAPI(
            base_url="https://www.dajintruck.com",
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            sign_key=os.getenv("SIGN_KEY"),
        )

    def test_get_access_token(self):
        """Test the retrieval of an access token from the API."""
        token = self.api.get_access_token()
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_get_vehicle_list(self):
        """Test the retrieval of the vehicle list from the API."""
        vehicles = self.api.get_vehicle_list()
        assert vehicles is not None
        assert isinstance(vehicles, dict)
        assert len(vehicles) > 0

    def test_get_vehicle_info(self):
        """Test the retrieval of vehicle information by vehicle ID."""
        vehicle_id = 7543
        vehicle_info = self.api.get_vehicle_info(vehicle_id)
        assert vehicle_info is not None
        assert isinstance(vehicle_info, dict)
        assert vehicle_info.get("id") == vehicle_id

    def test_get_tire_list(self):
        """Test the retrieval of the tire list from the API."""
        tires = self.api.get_tire_list()
        assert tires is not None
        assert isinstance(tires, dict)
        assert len(tires) > 0

    def test_get_tires_info_by_vehicle(self):
        """Test the retrieval of tire information by vehicle ID."""
        vehicle_id = 7543
        tires_info = self.api.get_tires_info_by_vehicle(vehicle_id)
        assert tires_info is not None
        assert isinstance(tires_info, dict)
        assert len(tires_info) > 0

    def test_get_tires_info_by_vehicle_invalid_id(self):
        """Test the retrieval of tire information by an invalid vehicle ID."""
        vehicle_id = 999999
        tires_info = self.api.get_tires_info_by_vehicle(vehicle_id)
        assert tires_info is None

    def test_get_tire_info(self):
        """Test the retrieval of tire information by tire ID."""
        tire_id = 47048
        tire_info = self.api.get_tire_info(tire_id)
        assert tire_info is not None
        assert isinstance(tire_info, dict)
        assert tire_info.get("id") == tire_id

    def test_get_tbox_list(self):
        """Test the retrieval of the tbox list from the API."""
        tbox_list = self.api.get_tboxes_list()
        assert tbox_list is not None
        assert isinstance(tbox_list, dict)
        assert len(tbox_list) > 0

    def test_get_tbox_info(self):
        """Test the retrieval of tbox information by tbox ID."""
        tbox_id = 8694
        tbox_info = self.api.get_tbox_info(tbox_id)
        assert tbox_info is not None
        assert isinstance(tbox_info, dict)
        assert tbox_info.get("id") == tbox_id

    def test_get_sensor_list(self):
        """Test the retrieval of the sensor list from the API."""
        sensors = self.api.get_sensor_list()
        assert sensors is not None
        assert isinstance(sensors, dict)
        assert len(sensors) > 0

    def test_get_sensor_info(self):
        """Test the retrieval of sensor information by sensor ID."""
        sensor_id = 48902
        sensor_info = self.api.get_sensor_info(sensor_id)
        assert sensor_info is not None
        assert isinstance(sensor_info, dict)
        assert sensor_info.get("id") == sensor_id

    def test_get_tire_brands(self):
        """Test the retrieval of tire brands from the API."""
        brands = self.api.get_tire_brands()
        assert brands is not None
        assert isinstance(brands, list)
        assert len(brands) > 0

    def test_get_tire_sizes(self):
        """Test the retrieval of tire sizes from the API."""
        sizes = self.api.get_tire_sizes()
        assert sizes is not None
        assert isinstance(sizes, list)
        assert len(sizes) > 0

    def test_get_vehicle_models(self):
        """Test the retrieval of vehicle models from the API."""
        models = self.api.get_vehicle_models()
        assert models is not None
        assert isinstance(models, list)
        assert len(models) > 0

    def test_get_axle_types(self):
        """Test the retrieval of axle types from the API."""
        axle_types = self.api.get_axle_types()
        assert axle_types is not None
        assert isinstance(axle_types, list)
        assert len(axle_types) > 0
