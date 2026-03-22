from enum import Enum


class APIRoutes(str, Enum):
    """Базовые маршруты API для шаблонного проекта."""

    AUTHENTICATE = "/authenticate"
    ORGANIZATIONS = "/organizations/"
    ORGANIZATIONS_RETRIEVE = "/organizations/{id}"

    # Devices
    DEVICES = "/devices/"
    DEVICES_METADATA = "/devices/{IMEI}"

    def __str__(self) -> str:
        return self.value
