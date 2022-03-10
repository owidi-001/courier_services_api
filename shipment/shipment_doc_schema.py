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
                coreapi.Field(
                    "distance",
                    required=False,
                    location="form",
                    schema=coreschema.Number(
                        description="""
                        Calculated distance between origin and destination in km <br> 
                        if the value is left empty, origin <code>lat</code>,<code>lng</code> 
                        and destination origin <code>lat</code>,<code>lng</code> must be provided
                        """,
                    ),
                ),
            ]
        if method.lower() == "patch":
            extra_fields = [
                coreapi.Field(
                    "shipment_id",
                    required=True,
                    location="form",
                    schema=coreschema.Integer(
                        description="<code>id</code> of shipment to cancel",
                    ),
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
                coreapi.Field(
                    "shipment_id",
                    required=True,
                    location="form",
                    schema=coreschema.Integer(),
                ),
                coreapi.Field(
                    "rating",
                    required=True,
                    location="form",
                    schema=coreschema.Number(maximum=5, minimum=0),
                ),
                coreapi.Field(
                    "message",
                    required=True,
                    location="form",
                    schema=coreschema.String(format="textarea"),
                ),
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields
