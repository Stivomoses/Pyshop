from django.db import models

# Create your models here.


class FeaturedBrand(models.Model):
    brand_name = models.CharField(max_length=15)
    brand_logo = models.ImageField(upload_to='brand_logos', default='')

    def __str__(self):
        return self.brand_name.capitalize()

    def delete(self):
        self.brand_logo.delete()
        super().delete()


class Category(models.Model):
    category_name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name.capitalize()


class Product(models.Model):

    bargainable_options = (
        ('No', 'No'),
        ('Yes', 'Yes')
    )

    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    brand_name = models.ForeignKey(
        FeaturedBrand, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    cover_image = models.ImageField(upload_to='product_images', default='')
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField(blank=True, null=True)
    is_price_bargainable = models.CharField(
        choices=bargainable_options, max_length=3, default='No')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def delete(self):
        self.cover_image.delete()
        super().delete()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.product.name

    def delete(self):
        self.image.delete()
        super().delete()


class SizeVariation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=20)

    def __str__(self):
        return self.size

# class Advertisement(models.Model):
#     advert = models.ImageField(upload_to='adverts', default='')


# class Trending(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
