# Generated by Django 3.1.5 on 2021-03-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='internshipType',
        ),
        migrations.AddField(
            model_name='comment',
            name='internshipType',
            field=models.CharField(choices=[('校外課程實習', '校外課程實習'), ('校外全職實習', '校外全職實習'), ('校內課程實習', '校內課程實習'), ('校內全職實習', '校內全職實習')], max_length=200, null=True),
        ),
    ]
