# Generated by Django 3.1.4 on 2020-12-29 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reframery', '0009_auto_20201229_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='validate_code',
            field=models.CharField(default='ozu2fwf7v5qo^4#zida*', max_length=255),
        ),
    ]
