from django.urls import path,include
from .views import UserSearchView,SigninViewSet,SignupViewset
from .views import (
    SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView,
    ListFriendsView, ListPendingFriendRequestsView
)
from rest_framework import routers



router = routers.SimpleRouter()
#as this url is already exist in other project so keep this url name same
router.register('postsignup', SignupViewset,basename='postsignup')
router.register('postSignIn', SigninViewSet, basename='postSignIn')

urlpatterns = [
    path('', include(router.urls)),   
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('send_friend_request/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('reject_friend_request/<int:pk>/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('pending_friend_requests/', ListPendingFriendRequestsView.as_view(), name='pending_friend_requests'),
]