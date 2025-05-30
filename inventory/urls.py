from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from .views import (
    inventory_list,
    product_detail,
    add_product,
    delete_product,
    inventory_update,  # ✅ TO‘G‘RI NOM
    dashboard,
)

urlpatterns = [
    path("", inventory_list, name='inventory_list'),
    path("product/<int:pk>/", product_detail, name='product_detail'),
    path("add_inventory/", add_product, name='add_inventory'),
    path("delete/<int:pk>/", delete_product, name='delete_inventory'),
    path("update/<int:pk>/", inventory_update, name='update_inventory'),  # ✅ TO‘G‘RI QATOR
    path("dashboard/", dashboard, name="dashboard"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]
