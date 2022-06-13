from django.db.models import Model


def get_table_headers(model: Model, exclude_id=False) -> list:
    """
    Получение заголовков для таблицы из модели

    Args:
        model (Model, optional): _description_. Defaults to None.

    Returns:
        Список заголовков
    """
    i = 0
    if exclude_id:
        i = 1
    fields = model._meta.fields[i:]
    table_columns = [model._meta.get_field(f.attname).verbose_name for f in fields]

    return table_columns
