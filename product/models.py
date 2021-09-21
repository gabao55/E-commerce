from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
from utils import utils

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    large_description = models.TextField()
    image = models.ImageField(
        upload_to='product_images/%Y/%m', blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    marketing_price = models.FloatField(verbose_name='Price')
    promotional_marketing_price = models.FloatField(default=0, verbose_name='Promotional Price')
    type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variable'),
            ('S', 'Simple'),
        )
    )

    def get_formated_price(self):
        return utils.price_format(self.marketing_price)
    get_formated_price.short_description = 'Price'

    def get_formated_promotional_price(self):
        return utils.price_format(self.promotional_marketing_price)
    get_formated_promotional_price.short_description = 'Promotional Price'

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.image:
            self.resize_image(self.image, max_image_size)

    def __str__(self):
        return self.name

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    inventory = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name or self.product

    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'