# Generated by Django 3.1.2 on 2020-10-28 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201027_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[(1, 'Electronics'), (2, 'Musical Instruments'), (3, 'Sports Equipment'), (4, 'No Category Specified')], default=4, max_length=64),
        ),
    ]