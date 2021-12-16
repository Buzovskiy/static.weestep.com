# Generated by Django 4.0 on 2021-12-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image360',
            name='image_360_path',
            field=models.CharField(max_length=255, null=True, verbose_name='Image 360 path'),
        ),
        migrations.AlterField(
            model_name='image360',
            name='vendor_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Product vendor code'),
        ),
    ]
