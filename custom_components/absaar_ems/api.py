"""API client for Absaar Inverter."""
import logging
import requests
import urllib3

from .const import BASE_URL

urllib3.disable_warnings()

_LOGGER = logging.getLogger(__name__)


class AbsaarAPI:
    """API client for Absaar EMS."""

    def __init__(self, username: str, password: str):
        """Initialize the API client."""
        self.username = username
        self.password = password
        self.token = None
        self.user_id = None

    def authenticate(self) -> bool:
        """Authenticate with the API and obtain token."""
        url = f"{BASE_URL}/dn/userLogin"
        headers = {
            "User-Agent": "okhttp-okgo/jeasonlzy",
            "Content-Type": "application/json;charset=utf-8",
        }
        payload = {"username": self.username, "password": self.password}

        try:
            response = requests.post(
                url, headers=headers, json=payload, verify=False, timeout=10
            )
            data = response.json()

            if response.status_code == 200 and "token" in data:
                self.token = data["token"]
                self.user_id = data["userId"]
                _LOGGER.debug("Successfully authenticated with Absaar API")
                return True
            else:
                _LOGGER.error("Authentication failed: %s", data)
                return False
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error during authentication: %s", e)
            return False

    def get_stations(self) -> dict:
        """Fetch station list."""
        if not self.token:
            _LOGGER.error("Not authenticated")
            return None

        url = f"{BASE_URL}/dn/power/station/listApp"
        headers = {"Authorization": str(self.token)}
        payload = {"userId": str(self.user_id)}

        try:
            response = requests.post(
                url, headers=headers, data=payload, verify=False, timeout=10
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error fetching stations: %s", e)
            return None

    def get_collectors(self, power_id: str) -> dict:
        """Fetch collector list for a station."""
        if not self.token:
            _LOGGER.error("Not authenticated")
            return None

        url = f"{BASE_URL}/dn/power/collector/listByApp"
        headers = {"Authorization": str(self.token)}
        payload = {"powerId": str(power_id)}

        try:
            response = requests.post(
                url, headers=headers, json=payload, verify=False, timeout=10
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error fetching collectors: %s", e)
            return None

    def get_inverter_data(self, power_id: str, inverter_id: str) -> dict:
        """Fetch inverter data."""
        if not self.token:
            _LOGGER.error("Not authenticated")
            return None

        url = f"{BASE_URL}/dn/power/inverterData/inverterDatalist"
        headers = {"Authorization": self.token}
        payload = {"powerId": power_id, "inverterId": inverter_id}

        try:
            response = requests.post(
                url, headers=headers, json=payload, verify=False, timeout=10
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error fetching inverter data: %s", e)
            return None

    def fetch_all_data(self) -> dict:
        """Fetch all data from the API."""
        stations_data = self.get_stations()

        if not stations_data or "rows" not in stations_data:
            _LOGGER.error("No stations found")
            return {}

        all_data = {"stations": []}

        for station in stations_data.get("rows", []):
            power_id = station["powerId"]
            station_info = {
                "power_id": power_id,
                "power_name": station["powerName"],
                "daily_power_generation": station.get("dailyPowerGeneration", 0),
                "total_power_generation": station.get("totalPowerGeneration", 0),
                "collectors": [],
            }

            collectors = self.get_collectors(power_id)
            if collectors and "rows" in collectors:
                for collector in collectors.get("rows", []):
                    inverter_id = collector["inverterId"]
                    inverter_data = self.get_inverter_data(power_id, inverter_id)

                    if inverter_data and "rows" in inverter_data and inverter_data["rows"]:
                        collector_info = {
                            "inverter_id": inverter_id,
                            "collector_name": collector.get("collectorName", "Unknown"),
                            "data": inverter_data["rows"][0],
                        }
                        station_info["collectors"].append(collector_info)

            all_data["stations"].append(station_info)

        return all_data
