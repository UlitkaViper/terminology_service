from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index),
    path('fill-db', view=views.fill_db, name='fill-db'),
    path('truncate-tables', view=views.truncate_tables, name='truncate-tables'),

    path('get-catalog-list', view=views.get_catalog_list, name='get-catalog-list'),
    path('get-catalog-on-date', view=views.get_catalog_on_date, name='get-catalog-on-date'),
    path(
        'get-elements-from-catalog',
        view=views.get_elements_from_catalog,
        name='get-elements-from-catalog'
    ),
    path(
        'get-elements-from-catalog-by-version',
        view=views.get_elements_from_catalog_by_version,
        name='get-elements-from-catalog-by-version'
    ),
    path(
        'validate-catalog-element-by-version',
        view=views.validate_catalog_element_by_version,
        name='validate-catalog-element-by-version'
    ),


    path(
        'update-element-by-id',
        view=views.update_element_by_id,
        name='update-element-by-id'
    ),
]
