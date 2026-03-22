from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DevicesMetaDataSchema(BaseModel):
    """Параметры запроса GET /devices/{IMEI}."""

    IMEI: int


class DevicesMetaDataResponseSchema(BaseModel):
    """Ответ от devices/{IMEI} endpoint."""

    class Cameras(BaseModel):
        cameraId: int
        name: str

    class DeviceMetaDataSchema(BaseModel):
        imei: str
        organizationId: int
        name: str
        groupId: int
        status: str
        iccid: str
        cameras: list["DevicesMetaDataResponseSchema.Cameras"]
        lat: float
        lon: float
        alt: float
        accuracy: int
        lastSeenOnline: str
        firmwareVersion: str
        deviceModel: str
        dataProfileId: int
        vehicleType: str

    data: DeviceMetaDataSchema
    requestId: UUID

    model_config = ConfigDict(extra="ignore")
