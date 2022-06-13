import factory
from main import tables


class CatalogElementFactory(factory.django.DjangoModelFactory):
    id = factory.Faker("pyint")
    catalog = factory.Faker("pyint")
    code = factory.fuzzy.FuzzyInteger(10000, 99999)
    value = factory.fuzzy.FuzzyInteger(1000, 9999)

    class Meta:
        model = tables.CatalogElement
