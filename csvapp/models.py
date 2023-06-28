from django.db import models
from datetime import date


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class SalesHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sales_num = models.PositiveSmallIntegerField()
    sales_date = models.DateField(default=date.today)

    def __str__(self):
        return self.product.name
