import coreapi
from rest_framework.schemas import AutoSchema


class ClientSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ["put", "post"]:
            extra_fields = [
                coreapi.Field("email", required=False, location="form"),
                coreapi.Field("phone_number", required=False, location="form"),
                coreapi.Field("username", required=False,
                              location="form", schema=None),
                coreapi.Field("avatar", required=False, location="form"),
                coreapi.Field("gender", required=False, location="form"),

            ]
        if method.lower() in ["patch"]:
            extra_fields = [
                coreapi.Field("avatar", required=False, location="form")
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields
