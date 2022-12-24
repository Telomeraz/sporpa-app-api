import pytest
from faker import Faker
from psycopg2.extras import DateTimeTZRange

from django.core.exceptions import ValidationError
from django.utils import timezone

from events.validators import validate_now_less_than_lower_value

fake = Faker()


@pytest.mark.parametrize(
    "lower",
    [fake.date_time_between(start_date="+1d", end_date="+15d")],
)
@pytest.mark.parametrize(
    "upper",
    [fake.date_time_between(start_date="+16d", end_date="+30d")],
)
def test_validate_now_less_than_lower_value(
    lower: timezone.datetime,
    upper: timezone.datetime,
) -> None:
    value = DateTimeTZRange(lower=lower, upper=upper)
    assert validate_now_less_than_lower_value(value) is None


@pytest.mark.parametrize(
    "lower",
    [fake.date_time_between(start_date="-15d", end_date="-1d")],
)
@pytest.mark.parametrize(
    "upper",
    [fake.date_time_between(start_date="+16d", end_date="+30d")],
)
def test_validate_now_less_than_lower_value_when_lower_is_less_than_now(
    lower: timezone.datetime,
    upper: timezone.datetime,
) -> None:
    value = DateTimeTZRange(lower=lower, upper=upper)
    with pytest.raises(ValidationError):
        validate_now_less_than_lower_value(value)
