from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin_view, name="signin"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("cabinet", views.cabinet_view, name="cabinet"),
    path("<int:user_id>/add_to_cart", views.add_to_cart_view, name="add_to_cart")
]
