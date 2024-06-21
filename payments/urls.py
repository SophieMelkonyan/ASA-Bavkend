from django.urls import path
from . import views

app_name = "payment"
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('create-checkout-session/<int:pk>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
