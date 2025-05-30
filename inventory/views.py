from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory
from .forms import AddInventoryForm, UpdateInventoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime

# HomePage (home_dark)
@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    return render(request, "inventory/home_dark.html", {
        "title": "All Products",
        "inventories": inventories
    })

# Product Detail Page (productdetail.html)
@login_required
def product_detail(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    return render(request, "inventory/productdetail.html", {
        "inventory": inventory,
        "title": "Product Details"
    })

# Add Product Page (add.html)
@login_required
def add_product(request):
    if request.method == "POST":
        form = AddInventoryForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.sales = float(product.cost_per_item) * float(product.quantity_sold)
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('inventory_list')
    else:
        form = AddInventoryForm()
    return render(request, "inventory/add.html", {
        "form": form,
        "title": "Add New Product"
    })

# Update Product (per_product.html)
@login_required
def inventory_update(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        form = UpdateInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            product = form.save(commit=False)
            product.sales = float(product.cost_per_item) * float(product.quantity_sold)
            product.last_sales_date = datetime.date.today()
            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_detail", pk=pk)
    else:
        form = UpdateInventoryForm(instance=inventory)
    return render(request, "inventory/inventory_update.html", {
        "form": form,
        "inventory": inventory,
        "title": "Update Product"
    })

# Delete
@login_required
def delete_product(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.warning(request, "Product deleted successfully!")
    return redirect("inventory_list")

# Dashboard Page (dashboard.html)
@login_required
def dashboard(request):
    inventories = Inventory.objects.all()
    total_stock = sum(i.quantity_in_stock for i in inventories)
    total_sales = sum(i.sales for i in inventories)
    low_stock = len([i for i in inventories if i.quantity_in_stock < 50])
    categories = set(i.category for i in inventories)

    return render(request, "inventory/dashboard.html", {
        "title": "Dashboard",
        "total_stock": total_stock,
        "total_sales": total_sales,
        "low_stock": low_stock,
        "category_count": len(categories)
    })
