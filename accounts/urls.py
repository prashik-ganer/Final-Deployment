from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.registrationPage, name="register"),
    path("login/", views.loginPage, name="login"),


    path("", views.home, name="home"),
    path("users/", views.userPage, name="user_page"),

    path("account/", views.accountSettings, name="account"),

    path("products/", views.products, name="products"),
    path("customer/<str:pk_test>", views.customer, name="customer"),
    
    path("create_order/", views.createOrder, name="create_order"),
    path("update_order/<str:pk>", views.updateOrder, name="update_order"),
    path("delete_order/<str:pk>", views.deleteOrder, name="delete_order"),
]
