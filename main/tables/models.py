from django.db import models

# Create your models here.


class Catalog(models.Model):
    # catalog_id = models.IntegerField("Идентификатор справочника", null=False)
    name = models.CharField("Наименование", max_length=100)
    short_name = models.CharField("Короткое наименование", max_length=20)
    description = models.CharField("Описание", max_length=250)
    version = models.CharField("Версия", null=False, max_length=20)
    version_start_date = models.DateField("Дата версии")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"


class CatalogElement(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name="Id каталога")
    code = models.CharField("Код элемента", null=False, max_length=20)
    value = models.CharField("Значение элемента", null=False, max_length=20)

    class Meta:
        verbose_name = "Элемент справочник"
        verbose_name_plural = "Элементы справочников"
