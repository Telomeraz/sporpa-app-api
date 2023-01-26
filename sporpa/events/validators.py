from psycopg2.extras import DateTimeTZRange

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext


def validate_now_less_than_lower_value(value: DateTimeTZRange) -> None:
    if value.lower <= timezone.datetime.now():
        raise ValidationError(gettext("Please select a further date."))
