from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from .views import (
    inventory_list,
    add_product,
    delete_product,
    update_product,
    dashboard,
    product_detail
)

urlpatterns = [
    path("", inventory_list, name='inventory_list'),
    path("product/<int:pk>/", product_detail, name='product_detail'),
    path("add_inventory/", add_product, name='add_inventory'),
    path("delete/<int:pk>/", delete_product, name='delete_inventory'),
    path("update/<int:pk>/", update_product, name='update_inventory'),
    path("dashboard/", dashboard, name="dashboard"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]
