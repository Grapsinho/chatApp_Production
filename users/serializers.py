from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    # Define serializer fields for email, username, and password
    email = serializers.CharField(max_length=80)
    password = serializers.CharField(min_length=8, write_only=True)  # Password won't be included in serialized output

    class Meta:
        model = User
        fields = ["email", "password", 'full_name', 'avatar']  # Fields to include in the serializer

    # Validate method to check if the email already exists in the database
    def validate(self, attrs):
        email_exist = User.objects.filter(email=attrs["email"]).exists()
        if email_exist:
            raise ValidationError("Email has already been used")  # Raise an error if the email is already in use
        return super().validate(attrs)

    # Create method to handle the creation of a new user
    def create(self, validated_data):
        password = validated_data.pop("password")  # Extract the password from validated data
        user = super().create(validated_data)  # Create a new user instance
        user.set_password(password)  # Set the user's password using set_password for encryption
        user.save()  # Save the user instance with the updated password
        return user  # Return the created user instance

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'avatar', 'bio']  # Update only allowed fields
        read_only_fields = ['email',]  # Prevent email modification through the API