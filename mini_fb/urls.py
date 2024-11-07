from django.urls import path
from .views import (ShowAllProfilesView, ShowProfilePageView, CreateProfileView,
                    CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView,
                    CreateFriendView, ShowFriendSuggestionsView, ShowNewsFeedView)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authenticate

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/', ShowProfilePageView.as_view(), name='show_own_profile'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('status/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/delete/<int:pk>/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
    path('login/', authenticate.LoginView.as_view(template_name='mini_fb/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', authenticate.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)