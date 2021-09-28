# Generated by Django 3.2.7 on 2021-09-28 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_auto_20210927_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobAdSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('index', models.FloatField()),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobad')),
            ],
        ),
    ]