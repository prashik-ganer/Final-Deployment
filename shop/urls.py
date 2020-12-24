from django.urls import path
from shop import views


urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/prod=<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("samplenew/", views.samplenew, name="samplenew"),
    path("signup/", views.handleSignup, name="handlesignup"),
    path("login/", views.handleLogin, name="handleLogin"),
    path("logout/", views.handleLogout, name="handleLogout"),
    path("category/", views.category, name="category"),
    path("category/<str:slug>", views.categorySlug, name="categorySlug"),
    path("stores/", views.stores, name="stores"),
    path("update_item/", views.updateItem, name="update_item"),
    path("qrcode/id=<int:order_id>", views.qrcode, name="qrcode"),
]
