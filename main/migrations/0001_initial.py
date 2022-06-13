# Generated by Django 4.0.5 on 2022-06-12 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('short_name', models.CharField(max_length=20, verbose_name='Короткое наименование')),
                ('description', models.CharField(max_length=250, verbose_name='Описание')),
                ('version', models.CharField(max_length=20, verbose_name='Версия')),
                ('version_start_date', models.DateField(verbose_name='дата начала действия справочника этой версии')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
        migrations.CreateModel(
            name='CatalogElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='Код элемента')),
                ('value', models.CharField(max_length=20, verbose_name='Значение элемента')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.catalog', verbose_name='catalog_id')),
            ],
            options={
                'verbose_name': 'Элемент справочник',
                'verbose_name_plural': 'Элементы справочников',
            },
        ),
    ]
