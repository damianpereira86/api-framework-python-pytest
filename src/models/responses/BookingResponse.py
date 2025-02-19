class BookingResponse:
    def __init__(self, **kwargs):
        self.first_name = kwargs.get("firstname")
        self.last_name = kwargs.get("lastname")
        self.total_price = kwargs.get("totalprice")
        self.deposit_paid = kwargs.get("depositpaid")
        self.booking_dates = kwargs.get("bookingdates")
        self.additional_needs = kwargs.get("additionalneeds")
