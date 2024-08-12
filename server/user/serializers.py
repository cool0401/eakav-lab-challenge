from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import get_ethereum_balance, validate_ethereum_address

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "wallet_address", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            wallet_address=self.validated_data["wallet_address"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if not validate_ethereum_address(user.wallet_address):
            raise serializers.ValidationError(
                {"wallet_address": "Invalid Ethereum address!"})

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    ethereum_balance = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "first_name", "last_name", "wallet_address", "ethereum_balance")

    def get_ethereum_balance(self, user):
        ethereum_address = user.wallet_address
        if ethereum_address:
            try:
                return get_ethereum_balance(ethereum_address)
            except Exception as e:
                return str(e)
        return None
