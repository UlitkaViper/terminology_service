## Элементы на главной расположены в порядке, указанном в задании

___
## Первые 2 кнопки доплонительные:

## **Заполнить бд** 
Заполняет базу рандомными данными, генерирует по 2 одинаковых справочника с разными версями
и по 25 элементов на каждый справочник. Всего добавляет по 10 справочников

> ## fill-db

## **Очистить базу** 
Удаляет данные из таблиц

> ## truncate-tables

___

## Основные методы:

## **Получить список каталогов** 
Получение списка справочников

> ## get-catalog-list

## **Список каталогов на дату** 
Получение списка справочников, актуальных на указанную дату

Принимает `Дату`

> ## get-catalog-on-date

## **Список элементов каталога №1** 
Получение элементов заданного справочника текущей версии 

> ## get-elements-from-catalog

## **Пока нет** 
Валидация элементов заданного справочника текущей версии 

> ## -------------

## **Список элементов каталога №2** 
Получение элементов заданного справочника указанной версии 

Принимает `Название справочника` - поле `Наименование` из таблицы справочников, а также `Версию справочника`
> ## get-elements-from-catalog-by-version

## **Пока нет** 
Валидация элемента заданного справочника по указанной версии

> ## -------------