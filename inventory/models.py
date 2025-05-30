from django.db import models
import datetime

class Inventory(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity_in_stock = models.IntegerField(null=False, blank=False)
    quantity_sold = models.IntegerField(null=False, blank=False)
    sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    stock_date = models.DateField(auto_now=True)
    last_sales_date = models.DateField(auto_now=True)
    
    category = models.CharField(max_length=100, null=True, blank=True, help_text="Kategoriya nomini kiriting")

    def __str__(self):
        return self.name

