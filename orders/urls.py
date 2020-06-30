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
    path("add_topings", views.add_topings_view, name="add_topings"),
    path("remove_item_from_cart", views.remove_item_from_cart_view, name="remove_item_from_cart"),
    path("order_placing", views.order_placing_view, name="order_placing"),
    path("change_order_status", views.change_order_status_view, name="change_order_status"),
    path("delete_order", views.delete_order_view, name="delete_order"),
    path("<int:order_id>", views.order, name="order"),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/orders/favicon.png'))
]
