from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest, User

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'].lower()
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


    def validate(self, data):
        from_user = self.context['request'].user  # Get the from_user from the request context

        try:
            to_user = User.objects.get(email=data['to_user_email'])
            data['to_user'] = to_user
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")

        if from_user == data['to_user']:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")

        data['from_user'] = from_user  # Add the from_user to the data
        return data

    def create(self, validated_data):
        validated_data.pop('to_user_email')
        return super().create(validated_data)


class FriendListSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'friend', 'timestamp']

    def get_friend(self, obj):
        request_user = self.context['request'].user
        if obj.from_user == request_user:
            return UserSerializer(obj.to_user).data
        return UserSerializer(obj.from_user).data


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_email = serializers.EmailField(source='from_user.email', read_only=True)
    to_user_email = serializers.EmailField(write_only=True)  # Make this field write-only

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'from_user_email', 'to_user', 'to_user_email', 'is_accepted', 'timestamp']
        read_only_fields = ['from_user', 'from_user_email', 'to_user', 'timestamp']

    def validate(self, data):
        from_user = self.context['request'].user

        try:
            to_user = User.objects.get(email=data['to_user_email'])
            data['to_user'] = to_user
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")

        if from_user == data['to_user']:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")

        return data

    def create(self, validated_data):
        validated_data.pop('to_user_email')  # Remove to_user_email before saving
        return super().create(validated_data)


