# Generated by Django 4.0 on 2021-12-24 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image360upload', '0031_alter_website_api_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateImages360Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('website', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='image360upload.website')),
            ],
        ),
    ]
