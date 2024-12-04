# Generated by Django 4.2.16 on 2024-12-04 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survei', '0020_alter_survei_ruang_lingkup_alter_survei_tipe_survei'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survei',
            name='ruang_lingkup',
            field=models.CharField(choices=[('Nasional', 'Nasional'), ('Provinsi', 'Provinsi'), ('Kota', 'Kota')], default='Nasional', max_length=255),
        ),
        migrations.AlterField(
            model_name='survei',
            name='wilayah_survei',
            field=models.JSONField(default=list),
        ),
    ]
