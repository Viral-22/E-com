from django.urls import path
from . import views
urlpatterns = [
    path("",views.Index,name="ShopHome"),
    path("about/",views.About,name="About"),
    path("tracker/",views.Tracker,name="Tracker"),
    path("contact/",views.contact,name="Contact Us"),
    path("bookview/<int:myid>",views.BookView,name="Book View"),
    path("checkout/",views.Checkout,name="Checkout"),
    path("search/",views.Search,name="Search"),
    path("signup/", views.handleSignUp, name="handleSignUp"),
    path("login/", views.handleLogin, name="handleLogin"),
    path("logout/", views.handleLogout, name="handleLogout"),
    path("paytm/",views.paytm,name="payment")
   # path("handlerequest/", views.handlerequest, name="HandleRequest"),
]