import factory
import factory.django
import factory.fuzzy
from allauth.account.models import EmailAddress

from accounts.models import User


class EmailAddressFactory(factory.django.DjangoModelFactory):
    verified = True

    class Meta:
        model = EmailAddress


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
    avatar = factory.django.ImageField(filename=factory.Faker("file_name", category="image"))
    birthdate = factory.Faker("date_of_birth")
    gender = factory.fuzzy.FuzzyChoice(User.Gender.choices, getter=lambda c: c[0])
    about = factory.Faker("text", max_nb_chars=User.about.field.max_length)
    email_address1 = factory.RelatedFactory(
        EmailAddressFactory,
        factory_related_name="user",
        primary=True,
        email=factory.SelfAttribute("..email"),
    )

    class Meta:
        model = User
