from django.db import models
import json

class Stock(models.Model):
    stock_symbol = models.CharField(max_length=20)
    last_checked = models.DateTimeField()
    last_price = models.DecimalField(decimal_places=2, max_digits=20)
    change = models.DecimalField(decimal_places=2, max_digits=20)

    def __str__(self):
        return self.name

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)