# Generated by Django 3.1.5 on 2021-03-29 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_auto_20210325_0953'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Intern',
            new_name='InternPerson',
        ),
    ]
