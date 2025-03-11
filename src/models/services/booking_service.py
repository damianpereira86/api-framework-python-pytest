from typing import List

from src.base.service_base import ServiceBase
from src.models.requests.booking.booking_model import BookingModel
from src.models.responses.base.response import Response
from src.models.responses.booking.booking_response import (
    BookingIdResponse,
    BookingDetails,
    BookingResponse,
)


class BookingService(ServiceBase):
    def __init__(self, store_name: str = None):
        super().__init__("/booking", store_name=store_name)

    def get_booking_ids(
        self, params: dict = None, config: dict = None
    ) -> Response[List[BookingIdResponse]]:
        config = config or self.default_config
        if params:
            config["params"] = params
        return self.get(self.url, config=config, response_model=List[BookingIdResponse])

    def get_booking(
        self, booking_id: int, config: dict | None = None
    ) -> Response[BookingDetails]:
        config = config or self.default_config
        return self.get(
            f"{self.url}/{booking_id}",
            config=config,
            response_model=BookingDetails,
        )

    def add_booking(
        self, booking: BookingModel, config: dict | None = None
    ) -> Response[BookingResponse]:
        config = config or self.default_config
        return self.post(
            self.url,
            booking,
            config=config,
            response_model=BookingResponse,
        )

    def update_booking(
        self, booking_id: int, booking: BookingModel, config: dict | None = None
    ) -> Response[BookingDetails]:
        config = config or self.default_config
        return self.put(
            f"{self.url}/{booking_id}",
            booking,
            config=config,
            response_model=BookingDetails,
        )

    def partial_update_booking(
        self, booking_id: int, booking: BookingModel, config: dict | None = None
    ) -> Response[BookingDetails]:
        config = config or self.default_config
        return self.patch(
            f"{self.url}/{booking_id}",
            booking,
            config=config,
            response_model=BookingDetails,
        )

    def delete_booking(
        self, booking_id: int, config: dict | None = None
    ) -> Response[BookingDetails]:
        config = config or self.default_config
        return self.delete(
            f"{self.url}/{booking_id}",
            config=config,
            response_model=BookingDetails,
        )
