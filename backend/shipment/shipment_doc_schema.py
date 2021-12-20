from rest_framework.schemas import AutoSchema
import coreapi


class CustomerShipmentSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() == 'post':
            extra_fields = [
                coreapi.Field("trip_id", required=True, location="form"),
                coreapi.Field("seats_number", required=True, location="form"),

            ]
        if method.lower() == "put":
            extra_fields = [
                coreapi.Field("book_id", required=True, location="form",
                              description="id of booking to cancel"),

            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class DriverShipmentSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() == "post":
            extra_fields = [
                coreapi.Field("trip_id", required=True, location="form"),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class FeedbackSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() == "post":
            extra_fields = [
                coreapi.Field("message", required=True, location="form"),
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields
