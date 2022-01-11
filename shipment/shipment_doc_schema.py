from typing import OrderedDict
import coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
import coreapi


class ShipmentSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() == "post":
            extra_fields = [
                coreapi.Field(
                    "origin",
                    required=True,
                    location="form",
                    schema=coreschema.Object(
                        required=True,
                        description="""properties - lat, lng, city, street,
                                    city, name.
                                    <code>street</code>, <code>city</code> and <code>name</code> are required""",
                    ),
                ),
                coreapi.Field(
                    "destination",
                    required=True,
                    location="form",
                    schema=coreschema.Object(
                        description="""properties - lat, lng, city, street,
                                    city, name.
                                    <code>street</code>, <code>city</code> and <code>name</code> are required""",
                    ),
                ),
                coreapi.Field(
                    "cargo",
                    required=True,
                    example="",
                    location="form",
                    schema=coreschema.Object(
                        description="""
                                    properties - size, nature.,
                                    nature options; <code>F</code> - fragile, <code>NF</code> - not fragile.
                                    Size options; <code>S</code> - small, <code>M</code> - medium,<code>L</code> - large.
                                    """,
                    ),
                ),
                coreapi.Field(
                    "vehicle",
                    required=True,
                    location="form",
                    schema=coreschema.Integer(
                        description="Vehicle id",
                    ),
                ),
            ]
        if method.lower() == "put":
            extra_fields = [
                coreapi.Field(
                    "book_id",
                    required=True,
                    location="form",
                    description="id of booking to cancel",
                ),
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
