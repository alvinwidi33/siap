# Generated by Django 5.1.1 on 2024-11-30 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survei', '0017_alter_survei_tipe_survei'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survei',
            name='tipe_survei',
            field=models.CharField(choices=[('Paper-based', 'Paper-based'), ('Digital', 'Digital'), ('Lainnya', 'Lainnya')], default='Paper-based', max_length=255),
        ),
    ]
