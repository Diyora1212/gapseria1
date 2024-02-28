from django.urls import path

from apps.gap.views import RoomListView, RoomDetailView, LikeOpinionView, login_view, register_view

app_name = 'gap'
urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('room/<pk>', RoomDetailView.as_view(), name='room'),
    path('like/<pk>', LikeOpinionView.as_view(), name='opinion-like'),
    path('login/', login_view, name='login-page'),
    path('register/', register_view, name='register-page'),

]
