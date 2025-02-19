from src.base.ServiceBase import ServiceBase
from src.models.request.BookingModel import BookingModel
from src.models.responses.Response import Response
from src.models.responses.BookingResponse import (
    BookingDetails,
    BookingResponse,
    BookingIdResponse,
)


class BookingService(ServiceBase[BookingDetails]):
    def __init__(self):
        super().__init__("/booking")
        # Default response model for most endpoints
        self._response_model = BookingDetails

    def get_booking_ids(
        self, params: dict = None, config: dict = None
    ) -> Response[list[BookingIdResponse]]:
        config = config or self.default_config
        if params:
            config["params"] = params
        original_model = self._response_model
        self._response_model = BookingIdResponse
        try:
            return self.get(self.url, config)
        finally:
            self._response_model = original_model

    def get_booking(
        self, booking_id: int, config: dict | None = None
    ) -> Response[BookingDetails]:
        config = config or self.default_config
        return self.get(f"{self.url}/{booking_id}", config)

    def add_booking(
        self, booking: BookingModel, config: dict | None = None
    ) -> Response[BookingResponse]:
        config = config or self.default_config
        # Temporarily override response model for this call
        original_model = self._response_model
        self._response_model = BookingResponse
        try:
            return self.post(self.url, booking, config)
        finally:
            # Restore original response model
            self._response_model = original_model

    def update_booking(
        self, booking_id: int, booking: BookingModel, config: dict | None = None
    ) -> Response[BookingDetails]:
        config = config or self.default_config
        return self.put(f"{self.url}/{booking_id}", booking, config)

    def partial_update_booking(
        self, booking_id: int, booking: BookingModel, config: dict | None = None
    ) -> Response[BookingDetails]:
        config = config or self.default_config
        return self.patch(f"{self.url}/{booking_id}", booking, config)

    def delete_booking(
        self, booking_id: int, config: dict | None = None
    ) -> Response[BookingDetails]:
        config = config or self.default_config
        return self.delete(f"{self.url}/{booking_id}", config)
