from django.contrib import admin
# from .models import Catalog, CatalogElement
import main.tables as tables
# Register your models here.

admin.site.register([tables.Catalog, tables.CatalogElement])
