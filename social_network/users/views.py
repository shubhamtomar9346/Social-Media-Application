from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, FriendListSerializer
from rest_framework import serializers

User = get_user_model()


# User Signup View
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(email=serializer.validated_data['email'].lower())


# User Login View
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


# User Search View
class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'username']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('q', None)  # Use 'q' as the search parameter
        if search_query:
            if '@' in search_query:
                queryset = queryset.filter(email__iexact=search_query)
            else:
                queryset = queryset.filter(username__icontains=search_query)
        return queryset


# Send a Friend Request
class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        time_threshold = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            from_user=user,
            timestamp__gte=time_threshold
        ).count()

        if recent_requests_count >= 3:
            raise serializers.ValidationError("You cannot send more than 3 friend requests within a minute.")

        serializer.save(from_user=user)


# Accept a Friend Request
class AcceptFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()

        if friend_request.to_user != request.user:
            return Response({"error": "You cannot accept this request."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.is_accepted = True
        friend_request.save()
        return Response({"status": "Friend request accepted."}, status=status.HTTP_200_OK)


# Reject a Friend Request
class RejectFriendRequestView(generics.DestroyAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def delete(self, request, *args, **kwargs):
        friend_request = self.get_object()

        if friend_request.to_user != request.user:
            return Response({"error": "You cannot reject this request."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.delete()
        return Response({"status": "Friend request rejected."}, status=status.HTTP_200_OK)


# List Friends
class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(
            (models.Q(from_user=user) | models.Q(to_user=user)) &
            models.Q(is_accepted=True)
        ).order_by('-timestamp')


# List Pending Friend Requests
class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, is_accepted=False).order_by('-timestamp')
