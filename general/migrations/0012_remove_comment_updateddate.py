# Generated by Django 3.1.5 on 2021-04-27 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0011_auto_20210427_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='updatedDate',
        ),
    ]
