import factory
import factory.django
import factory.fuzzy

from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    birthdate = factory.Faker("date_of_birth")
    gender = factory.fuzzy.FuzzyChoice(User.Gender.choices, getter=lambda c: c[0])
    about = factory.Faker("text", max_nb_chars=600)

    class Meta:
        model = User
