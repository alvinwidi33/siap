# Generated by Django 4.1 on 2024-10-07 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataKlien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_klien', models.CharField(max_length=50)),
                ('nama_perusahaan', models.CharField(max_length=100)),
                ('daerah', models.TextField()),
                ('harga_survei', models.IntegerField()),
            ],
        ),
    ]
