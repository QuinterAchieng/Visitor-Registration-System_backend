from rest_framework import serializers
from .models import AuditLog
from .models import Visitor, Purpose, Department


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class VisitorSerializer(serializers.ModelSerializer):

    purpose = serializers.CharField()

    class Meta:
        model = Visitor
        fields = [
            "id",
            "full_name",
            "id_number",
            "contact",
            "visitor_type",
            "organization",
            "department",
            "purpose",
            "expected_duration",
            "items_carried"
        ]

        read_only_fields = (
            "check_in_time",
            "check_out_time",
            "checked_out",
            "checked_out_by",
            "recorded_by"
        )

      # Contact Validation (STRICT Production Safe Version)
    def validate_contact(self, value):

        if not value:
            raise serializers.ValidationError("Contact is required")

        if not value.isdigit():
            raise serializers.ValidationError("Contact must contain numbers only")

        if len(value) < 9 or len(value) > 15:
            raise serializers.ValidationError("Contact number length is invalid")

        return value

    # ID Number Validation
    def validate_id_number(self, value):

        if not value.isdigit():
            raise serializers.ValidationError("ID number must contain digits only")

        return value

    def create(self, validated_data):

        purpose_name = validated_data.pop("purpose").strip()

        purpose_obj, created = Purpose.objects.get_or_create(
            name__iexact=purpose_name,
            defaults={"name": purpose_name}
        )

        validated_data["purpose"] = purpose_obj

        return super().create(validated_data)