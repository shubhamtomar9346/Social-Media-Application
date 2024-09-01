from django.contrib import admin
from django.urls import path
from users.views import UserSignupView, UserLoginView, UserSearchView, SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/accept/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/reject/<int:pk>/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-requests/pending/', ListPendingRequestsView.as_view(), name='list-pending-requests'),
]
