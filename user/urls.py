from .views import RegistrationView, login_view,  ValidateUserLink,ProfileView,update_profile,delete_profile,create_post,create_story
from django.urls import path


app_name = "user"

urlpatterns = [
    path("", RegistrationView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path("<int:pk>/<str:token>/", ValidateUserLink.as_view(), name="verify"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", update_profile, name="update_profile"),
    path("profile/delete/", delete_profile, name="delete_profile"),
    path('create_post/', create_post, name='create_post'),
    path('create_story/', create_story, name='create_story'),

]