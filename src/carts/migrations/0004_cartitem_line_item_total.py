# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 04:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_auto_20170208_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='line_item_total',
            field=models.DecimalField(decimal_places=2, default=19.99, max_digits=10),
            preserve_default=False,
        ),
    ]
