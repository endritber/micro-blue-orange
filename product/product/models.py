from django.db import models
from common.models import AutoCreateUpdateMixin
from autoslug import AutoSlugField
import uuid
import os


def product_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/product/', filename)


class Category(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='name')
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    image = models.ImageField(max_length=255, upload_to=product_image_file_path)

    class Meta:
        verbose_name = 'product'

    def __str__(self) -> str:
        return self.title
