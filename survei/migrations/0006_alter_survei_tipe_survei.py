# Generated by Django 5.1.2 on 2024-11-13 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survei', '0005_alter_survei_tipe_survei'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survei',
            name='tipe_survei',
            field=models.CharField(choices=[('Digital', 'Digital'), ('Paper-based', 'Paper-based'), ('Lainnya', 'Lainnya')], default='Paper-based', max_length=255),
        ),
    ]
