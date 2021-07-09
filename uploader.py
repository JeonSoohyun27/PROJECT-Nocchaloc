import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nocchaloc.settings")
django.setup()

from products.models import Product, Category, ProductType

CSV_PATH_PRODUCTS = './nocchaloc_db - products.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Product.objects.create(
            name            = row[0],
            price           = row[1],
            description     = row[2],
            main_image_url    = row[3],
            hover_image_url   = row[4],
            is_new          = row[5],
            stock           = row[6],
            view_count      = row[7],
            category        = Category.objects.get(id=row[10]),
            product_type    = ProductType.objects.get(id=row[11])


        )