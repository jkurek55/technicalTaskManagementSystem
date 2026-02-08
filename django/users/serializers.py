from rest_framework import serializers

from django.contrib.auth import get_user_model

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")
        read_only_fields = fields
