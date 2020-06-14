from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin_view, name="signin"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("cabinet", views.cabinet_view, name="cabinet"),
    path("add_to_cart", views.add_to_cart_view, name="add_to_cart"),
    path("remove_item_from_cart", views.remove_item_from_cart_view, name="remove_item_from_cart"),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/orders/favicon.png'))
]
