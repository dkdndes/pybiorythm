from rest_framework import serializers
from datetime import datetime


class BiorhythmRequestSerializer(serializers.Serializer):
    """Serializer for biorhythm calculation request."""

    birthdate = serializers.DateField(
        help_text="Birth date in YYYY-MM-DD format (e.g., 1990-05-15)"
    )
    target_date = serializers.DateField(
        required=False,
        help_text="Target date for calculation (defaults to today if not provided)",
    )
    days = serializers.IntegerField(
        default=30,
        min_value=1,
        max_value=1095,  # Maximum 3 years
        help_text="Number of days to calculate (1-1095, default: 30)",
    )

    def validate_birthdate(self, value):
        """Validate that birthdate is not in the future."""
        if value > datetime.now().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value

    def validate_target_date(self, value):
        """Validate target date if provided."""
        if value and value < datetime(1900, 1, 1).date():
            raise serializers.ValidationError(
                "Target date cannot be before 1900-01-01."
            )
        return value


class BiorhythmResponseSerializer(serializers.Serializer):
    """Serializer for biorhythm calculation response."""

    # This is just for documentation purposes
    # The actual response will be the PyBiorythm JSON output
    pass
