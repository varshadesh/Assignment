from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from users.models import user,FriendRequest
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer,FriendRequestSerializer,UserLimitedSerializer
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model
import re
import bcrypt
from django.utils import timezone  # Ensure correct import
from datetime import timedelta
from django.utils.timezone import now
# Create your views here.


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# generating a hash password
def create_hashed_password(password):
    # password = b"SuperSercet34"
    # Encode password into a readable utf-8 byte code:
    password = password.encode('utf-8')
    # Hash the ecoded password and generate a salt: 
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode('UTF-8')

class SignupViewset(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_data = request.data
        n_data = None
        msg=''
        # Validate email format
        email = user_data.get("email")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            msg = "Invalid email format."
            return Response({"msg": msg, "data": n_data})

        try:
            user.objects.get(email=user_data["email"])          
            msg = "Email is already exist"          
        except user.DoesNotExist:

                create_user = user(
                    name=user_data["name"],
                    email=user_data["email"],
                    password=create_hashed_password(user_data["password"]),
                  #  username=user_data["email"],                   
                )
                create_user.save()
                print("", create_user)
                print(create_user.email)
                
                msg = "Congratulation!! Your registration is Successful! "
            
                serializer = UserSerializer(create_user)
                n_data = serializer.data          
        return Response({"msg": msg})



from datetime import datetime,timezone
# post for sign in
#token=Token
# used viewset for get method is not allowed
User = get_user_model()  # Get the user model

class SigninViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        user_data = request.data
        print("API IS HEATING")
        response_data = {"msg": "", "user_id": None, "data": None}

        try:
            # Get a user by its email with case insensitive
            record = user.objects.get(email__iexact=user_data.get("email"))
        except User.DoesNotExist:
            # Return response if user doesn't exist
            response_data['msg'] = "User doesn't exist."
            return Response(response_data)

        input_password = user_data.get('password')
        password_in_db = record.password

        # Check if the password matches
        if bcrypt.checkpw(input_password.encode('UTF-8'), password_in_db.encode('UTF-8')):
            # If password is valid, then send login successful response
            response_data['msg'] = "Login Successful"
            response_data['data'] = user_data["email"]
            example = UserLimitedSerializer()
            example.user = record.id
            token, _ = Token.objects.get_or_create(user=record)
           
            response_data['token'] = str(token.key)
            response_data['user_id'] = example.user
        else:
            # If password is not valid, then send this response
            response_data['msg'] = "Please check your password."

        return Response(response_data)



class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserLimitedSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.query_params.get('search', '')

        if search_keyword:
            if user.objects.filter(email__iexact=search_keyword).exists():
                return queryset.filter(email__iexact=search_keyword)
            return queryset.filter(name__icontains=search_keyword)
        
        return queryset



class SendFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def create(self, request, *args, **kwargs):
        sender = request.user
        receiver_email = request.data.get('receiver')
        try:
            receiver = user.objects.get(email=receiver_email)
        except User.DoesNotExist:
            return Response({'detail': 'Receiver not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check rate limit
        one_minute_ago = now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(sender=sender, timestamp__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({'detail': 'Rate limit exceeded. Try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Create friend request
        friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
        if not created:
            return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

class AcceptFriendRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        if friend_request.receiver != request.user:
            return Response({'detail': 'You cannot accept this friend request.'}, status=status.HTTP_403_FORBIDDEN)

        friend_request.accepted = True
        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data)

class RejectFriendRequestView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def delete(self, request, *args, **kwargs):
        friend_request = self.get_object()
        if friend_request.receiver != request.user:
            return Response({'detail': 'You cannot reject this friend request.'}, status=status.HTTP_403_FORBIDDEN)

        friend_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListFriendsView(generics.ListAPIView):
    queryset = user.objects.all()
    serializer_class = UserLimitedSerializer
    permission_classes = [IsAuthenticated]
  


    @api_view(['GET'])
    def getallfriends(self, request):
        try:
            users = user.objects.all()
            # print("SQL Query:", COA.query)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except user.DoesNotExist:
            return Response(status=404)
    # def get_queryset(self):
    #     user = self.request.user
    #     friends = user.objects.filter(
    #         Q(sent_friend_requests__receiver=user, sent_friend_requests__accepted=True) |
    #         Q(received_friend_requests__sender=user, received_friend_requests__accepted=True)
    #     ).distinct()
    #     return friends

class ListPendingFriendRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(receiver=user, accepted=False)