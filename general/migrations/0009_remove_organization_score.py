# Generated by Django 3.1.5 on 2021-04-02 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0008_auto_20210329_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='score',
        ),
    ]
