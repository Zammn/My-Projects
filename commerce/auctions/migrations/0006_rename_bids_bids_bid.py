# Generated by Django 4.1.5 on 2023-01-26 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='bids',
            new_name='bid',
        ),
    ]
