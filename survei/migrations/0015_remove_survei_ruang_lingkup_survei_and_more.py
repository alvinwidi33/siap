# Generated by Django 4.2.16 on 2024-12-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survei', '0014_alter_survei_tipe_survei'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survei',
            name='ruang_lingkup_survei',
        ),
        migrations.AddField(
            model_name='survei',
            name='ruang_lingkup',
            field=models.CharField(choices=[('Kabupaten/Kota', 'Kabupaten/Kota'), ('Provinsi', 'Provinsi'), ('Nasional', 'Nasional')], default='Nasional', max_length=255),
        ),
        migrations.AlterField(
            model_name='survei',
            name='tipe_survei',
            field=models.CharField(choices=[('Lainnya', 'Lainnya'), ('Paper-based', 'Paper-based'), ('Digital', 'Digital')], default='Paper-based', max_length=255),
        ),
    ]
