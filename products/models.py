from django.db                  import models
from django.db.models.deletion  import CASCADE

from users.models               import User

class Product(models.Model):
    name            = models.CharField(max_length=45)
    price           = models.DecimalField(max_digits=18, decimal_places=2)
    description     = models.TextField()
    main_image_url  = models.URLField()
    hover_image_url = models.URLField()
    is_new          = models.BooleanField()
    stock           = models.IntegerField()
    view_count      = models.IntegerField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    product_type    = models.ForeignKey('ProductType', on_delete=models.CASCADE)
    category        = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class ProductType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'product_types'

class Option(models.Model):
    name   = models.CharField(max_length=45)
    price  = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'options'

class Image(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.URLField()

    class Meta:
        db_table = 'images'

class Video(models.Model):
    name      = models.CharField(max_length=45)
    video_url = models.URLField()

    class Meta:
        db_table = 'videos'

class Review(models.Model):
    user        = models.ForeignKey(User, on_delete=CASCADE)
    product     = models.ForeignKey(Product, on_delete=CASCADE)
    comment     = models.CharField(max_length=200,blank=False,null=False)
    score       = models.DecimalField(max_digits=2,decimal_places=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Mete:
        db_table = 'reviews'
