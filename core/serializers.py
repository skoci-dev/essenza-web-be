from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile


class FlexibleImageField(serializers.Field):
    """
    Custom field that accepts both file uploads and string paths.
    Used for update operations where existing files can be kept (as strings)
    or replaced (as file uploads).
    """

    def to_internal_value(self, data) -> None | UploadedFile | str:
        """
        Convert input data to internal value.
        Accepts:
        - UploadedFile objects (new uploads)
        - String paths (existing files)
        - None or "null" string (to clear the field)
        """
        # Handle None or "null" string
        if data is None or data == "null" or data == "":
            return None

        # Handle file upload
        if isinstance(data, UploadedFile):
            return data

        # Handle string path (existing file)
        if isinstance(data, str):
            return data.lstrip("/")

        raise serializers.ValidationError(
            "Invalid input type. Expected a file upload or file path string."
        )

    def to_representation(self, value) -> str | None:
        """Convert internal value to representation."""
        return str(value) if value else None
