from django.db import models

class Stock(models.Model):
    stock_symbol = models.CharField(max_length=20)
    last_checked = models.DateTimeField()
    last_price = models.DecimalField(decimal_places=2)
    low = models.DecimalField(decimal_places=2)
    high = models.DecimalField(decimal_places=2)
    change = models.DecimalField(decimal_places=2)

    def __str__(self):
        return self.name