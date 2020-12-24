from django.urls import path
from seller import views


urlpatterns = [
    path("", views.home, name="seller"),
    path("<int:seller_profile>", views.seller_profile, name="seller"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("products", views.products, name="products"),
    path("tracker/<str:status>", views.sellerTracker, name="sellerTracker"),
    path("qrcode", views.qrcode, name="qrcode"),
    path("scanqr", views.scanqr, name="scanqr"),
    path("update_status/<str:status>", views.updateStatus, name="updateStatus"),
]
