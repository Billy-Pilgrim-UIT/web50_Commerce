# Generated by Django 3.1.2 on 2020-11-02 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageURL',
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
    ]
