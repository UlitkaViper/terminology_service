from datetime import datetime

from .factories import CatalogElementFactory, CatalogFactory
from main import tables
from .utils import get_table_headers

from django.shortcuts import render
from django.db.models import Max
from django.core.paginator import Paginator

# Create your views here.

CATALOG_FIELDS = [f.attname for f in tables.Catalog._meta.fields]
CATALOG_ELEMENT_FIELDS = [f.attname for f in tables.CatalogElement._meta.fields]


def index(request):
    return render(request, 'main/home.html')


def fill_db(request):
    """
    Функция для заполнения базы данными
    Создается по 2 одинковых справочника с разными версиями
    Для каджого справочника создается по 25 элементов

    Args:
        request

    Returns:
        Сообщение об успешном/неуспешном выполнении
    """

    response_data = {
        "message": None,
        "table_data": None,
        "table_headers": None,
        "error": None
    }
    try:
        last_catalog_id = tables.Catalog.objects.count()
        last_element_id = tables.CatalogElement.objects.count()
        for i in range(10):
            if i % 2 != 0:
                catalog = CatalogFactory(
                    id=last_catalog_id + i,
                    name=catalog.name,  # noqa
                    short_name=catalog.short_name,  # noqa
                    description=catalog.description,  # noqa
                )
            else:
                catalog = CatalogFactory(id=last_catalog_id + i)

            for j in range(25):
                CatalogElementFactory(
                    id=last_element_id,
                    catalog=catalog
                )
                last_element_id += 1
    except Exception as e:
        response_data["message"] = "Произошла ошибка"
        response_data["error"] = e
        return render(request, 'main/main_response_page.html', response_data)

    response_data["message"] = "Таблицы успешно заполнены"
    return render(request, 'main/main_response_page.html', response_data)


def truncate_tables(request):
    """
    Удаление данных из таблиц

    Args:
        request

    Returns:
        Сообщение об успешном/неуспешном выполнении
    """

    response_data = {
        "message": None,
        "table_data": None,
        "table_headers": None,
        "error": None
    }
    if request.method == "GET":
        try:
            tables.Catalog.objects.all().delete()
            tables.CatalogElement.objects.all().delete()
        except Exception as e:
            response_data["message"] = "Произошла ошибка"
            response_data["error"] = e
            return render(request, 'main/truncate_tables.html', response_data)

        response_data["message"] = "Таблицы успешно очищены"
        return render(request, 'main/main_response_page.html', response_data)


def get_catalog_list(request):
    """
    Получение списка справочников

    Args:
        request

    Returns:
        Список справочников
    """

    if request.method == "GET":
        try:
            table_data = tables.Catalog.objects.values_list(*CATALOG_FIELDS)
            table_headers = get_table_headers(tables.Catalog)
        except Exception as e:
            return render(
                request,
                'main/main_response_page.html',
                {"error": e, "message": "Данные не получены"}
            )

        # Пагинация
        p = Paginator(table_data, 10)
        page = request.GET.get('page')
        elements = p.get_page(page)

        response_data = {
            "message": "Данные успешно получены",
            "table_data": elements,
            "table_headers": table_headers,
        }
        return render(request, 'main/main_response_page.html', response_data)


def get_catalog_on_date(request):
    """
    Получение списка справочников, актуальных на указанную дату

    Здесь актуальный справочник выбирается по максимальной дате для этого справочника,
    подразумевая, что у каждой последующей даты версия становится больше.
    Сделал так, потому что не уверен, что выбор максимальной версии в формате хх.хх.хх
    всегда будет возвращать правльный результат

    Args:
        request

    Raises:
        TypeError: получена пустая дата

    Returns:
        Список справочников, актуальных на указанную дату
    """

    if request.method == "GET":
        try:
            if not request.GET.get("selected-date"):
                raise TypeError("Введена пустая дата")
            date = datetime.strptime(request.GET.get("selected-date"), "%Y-%m-%d").date()
            catalogs_with_max_date = (
                tables.Catalog.objects
                .filter(version_start_date__lt=date)
                .values_list(
                    'name',
                )
                .annotate(date=Max('version_start_date'))
            )
            names = [el[0] for el in catalogs_with_max_date]
            vers_date = [el[1] for el in catalogs_with_max_date]
            table_data = (
                tables.Catalog.objects
                .filter(
                    name__in=names,
                    version_start_date__in=vers_date,
                )
                .values_list(
                    *CATALOG_FIELDS
                )
            )
            table_headers = get_table_headers(tables.Catalog)

            # Пагинация
            p = Paginator(table_data, 10)
            page = request.GET.get('page')
            elements = p.get_page(page)

        except Exception as e:
            return render(
                request,
                'main/main_response_page.html',
                {"error": e, "message": "Данные не получены"}
            )

        response_data = {
            "message": "Данные успешно получены",
            "table_data": elements,
            "table_headers": table_headers,
            "selected_date": date,
        }
        return render(request, 'main/main_response_page.html', response_data)


def get_elements_from_catalog(request):
    """
    Получение элементов заданного справочника текущей версии

    Args:
        request

    Raises:
        TypeError: Получен пустой справочник
        ValueError: Неверный тип идентификатора справочника

    Returns:
        Список элементов справочника текущей версии
    """

    if request.method == "GET":
        try:
            if not request.GET.get("selected-catalog"):
                raise TypeError("Введен пустой справочник")

            catalog_id = int(request.GET.get("selected-catalog"))
            current_catalog = (
                tables.Catalog.objects
                .filter(
                    id=catalog_id,
                    version_start_date__lte=datetime.now().date()
                )
                .order_by('-version_start_date')
                .values_list('id')
                .first()
            )
            if not current_catalog:
                return render(
                    request,
                    'main/main_response_page.html',
                    {"message": "Нет данных по указанному справочнику"}
                )

            catalog_elements = (
                tables.CatalogElement.objects
                .filter(
                    catalog_id=current_catalog[0],
                )
                .values_list(*CATALOG_ELEMENT_FIELDS)
            )

            # Пагинация
            p = Paginator(catalog_elements, 10)
            page = request.GET.get('page')
            elements = p.get_page(page)

            table_headers = get_table_headers(tables.CatalogElement)

        except ValueError:
            error = "Неверный тип идентификатора каталога"
            return render(
                request,
                'main/main_response_page.html',
                {"error": error, "message": "Данные не получены"}
            )
        except Exception as e:
            return render(
                request,
                'main/main_response_page.html',
                {"error": e, "message": "Данные не получены"}
            )

        response_data = {
            "message": "Данные успешно получены",
            "table_data": elements,
            "table_headers": table_headers,
            "catalog_id": catalog_id,
        }
        return render(request, 'main/main_response_page.html', response_data)


def get_elements_from_catalog_by_version(request):
    """
    Получение элементов заданного справочника указанной версии

    Args:
        request

    Raises:
        TypeError: Переданы пустые данные
        ValueError: Неверный тип идентификатора каталога или версии

    Returns:
        Список элементов справочника указанной версии
    """

    if request.method == "GET":
        try:
            if not request.GET.get("selected-catalog") or not request.GET.get("selected-version"):
                raise TypeError("Переданы пустые параметры")

            catalog_id = request.GET["selected-catalog"].rstrip(" ").rstrip("\t")
            catalog_version = request.GET["selected-version"].rstrip(" ").rstrip("\t")
            catalog_elements = (
                tables.CatalogElement.objects
                .select_related('catalog')
                .filter(
                    catalog__name=catalog_id,
                    catalog__version=catalog_version,
                    catalog__version_start_date__lte=datetime.now().date()
                )
                .order_by('-catalog__version_start_date')
                .values_list(*CATALOG_ELEMENT_FIELDS)
            )

            if not catalog_elements:
                return render(
                    request,
                    'main/main_response_page.html',
                    {"message": "Нет данных по указанным параметрам"}
                )

            # Пагинация
            p = Paginator(catalog_elements, 10)
            page = request.GET.get('page')

            elements = p.get_page(page)
            table_headers = get_table_headers(tables.CatalogElement)

        except ValueError:
            error = "Неверный тип идентификатора каталога"
            return render(
                request,
                'main/main_response_page.html',
                {"error": error, "message": "Данные не получены"}
            )
        except Exception as e:
            return render(
                request,
                'main/main_response_page.html',
                {"error": e, "message": "Данные не получены"}
            )

        response_data = {
            "message": "Данные успешно получены",
            "table_data": elements,
            "table_headers": table_headers,
            "catalog_id": catalog_id,
            "catalog_version": catalog_version,
        }
        return render(request, 'main/main_response_page.html', response_data)
