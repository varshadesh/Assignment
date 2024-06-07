from rest_framework import serializers

from users.models import user,FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields =['name','email','password']


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'timestamp', 'accepted']


class UserLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['name', 'email']


class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['name']