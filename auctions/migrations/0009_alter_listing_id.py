# Generated by Django 5.0 on 2024-01-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]