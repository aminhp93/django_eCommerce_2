# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_cart_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50),
        ),
    ]
