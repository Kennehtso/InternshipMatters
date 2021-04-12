# Generated by Django 3.1.5 on 2021-04-12 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_auto_20210412_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='unitName',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='unitType',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='subsidy',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
