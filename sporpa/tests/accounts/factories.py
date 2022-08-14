import factory
import factory.django
import factory.fuzzy

from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
    avatar = factory.django.ImageField(filename=factory.Faker("file_name", category="image"))
    birthdate = factory.Faker("date_of_birth")
    gender = factory.fuzzy.FuzzyChoice(User.Gender.choices, getter=lambda c: c[0])
    about = factory.Faker("text", max_nb_chars=User.about.field.max_length)
    has_verified_email = True

    class Meta:
        model = User
