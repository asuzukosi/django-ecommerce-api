from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(models.Model):
    name = models.CharField(max_length=225)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}'

    def get_image_url(self):
        if self.image:
            return "http://127.0.0.1:8000/" + self.image.url

        else:
            return ""

    def get_thumbnail_url(self):
        if self.thumbnail:
            return "http://127.0.0.1:8000/" + self.thumbnail.url

        elif self.image:
            self.thumbnail = self.make_thumbnail(self.image)
            return "http://127.0.0.1:8000/" + self.thumbnail.url
        else:
            return ""

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail




