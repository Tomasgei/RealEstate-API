# Generated by Django 3.2.9 on 2021-11-30 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('UpdateDate', models.CharField(max_length=50)),
                ('ProjectId', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('index', models.IntegerField(primary_key=True, serialize=False)),
                ('updateDate', models.DateField()),
                ('flatNumber', models.CharField(max_length=10)),
                ('roomsNumber', models.IntegerField(null=True)),
                ('floorsNumber', models.IntegerField(null=True)),
                ('flatArea', models.FloatField()),
                ('balconyTerraceArea', models.FloatField(null=True)),
                ('totalArea', models.FloatField(null=True)),
                ('salesPrice', models.FloatField(null=True)),
                ('propStatus', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updateDate', models.DateField()),
                ('propStatus', models.CharField(max_length=20)),
                ('flatNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scraping_client.property')),
            ],
        ),
    ]