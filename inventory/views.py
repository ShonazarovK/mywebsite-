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

    # Importlar
    import plotly.graph_objs as go
    from plotly.offline import plot

    # Best Performing Product – Bar Chart
    product_names = [i.name for i in inventories]
    product_sales = [i.quantity_sold for i in inventories]
    bar = go.Bar(x=product_names, y=product_sales, marker_color='royalblue')
    bar_layout = go.Layout(
        title='Best Performing Product',
        xaxis=dict(title='Product name'),
        yaxis=dict(title='Quantity sold'),
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='#f8fafc')
    )
    best_chart_html = plot(go.Figure(data=[bar], layout=bar_layout), output_type='div')

    # Product Stock Overview – Pie Chart
    pie = go.Pie(
        labels=product_names,
        values=[i.quantity_in_stock for i in inventories],
        marker=dict(colors=['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#6366f1']),
        textinfo='percent+label'
    )
    pie_layout = go.Layout(
        title='Product Stock Overview',
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='#f8fafc'),
    )
    pie_chart_html = plot(go.Figure(data=[pie], layout=pie_layout), output_type='div')

    return render(request, "inventory/dashboard.html", {
        "title": "Dashboard",
        "total_stock": total_stock,
        "total_sales": total_sales,
        "low_stock": low_stock,
        "category_count": len(categories),
        "best_performing_product": best_chart_html,
        "most_product_in_stock": pie_chart_html,
    })
