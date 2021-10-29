from product.models import Product
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Demand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    total_amount = models.PositiveIntegerField()
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Approved'),
            ('R', 'Rejected'),
            ('C', 'Created'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finished'),
        )
    )

    def __str__(self):
        return f'Request N. {self.pk}'

class DemandItem(models.Model):
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    amount = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.demand}'s item"

    class Meta:
        verbose_name = 'Request item'
        verbose_name_plural = 'Request items'