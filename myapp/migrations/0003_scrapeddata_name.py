# Generated by Django 5.1.1 on 2024-10-12 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_scrapeddata_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapeddata',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
