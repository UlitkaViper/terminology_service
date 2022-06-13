import factory
import factory.fuzzy
# from main.models import Catalog
from main import tables


class CatalogFactory(factory.django.DjangoModelFactory):
    # Доп атрибуты для генерации полей
    words = factory.Faker("words", nb=3)
    num_for_ver = factory.List([factory.fuzzy.FuzzyInteger(0, 100) for i in range(3)])

    id = factory.Faker("pyint")
    # catalog_id = factory.Faker("pyint")
    name = factory.LazyAttribute(lambda obj: " ".join(w for w in obj.words))
    short_name = factory.LazyAttribute(lambda obj: "".join(w[0].capitalize() for w in obj.words))
    description = factory.Faker("sentence", nb_words=5)
    version = factory.LazyAttribute(lambda obj: ".".join(str(n) for n in obj.num_for_ver))
    version_start_date = factory.Faker("date_object")

    class Meta:
        model = tables.Catalog
        exclude = ("words", "num_for_ver")
