# Generated by Django 5.0 on 2024-01-03 13:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchList',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchList', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='imageurl',
            field=models.CharField(max_length=5000),
        ),
    ]
