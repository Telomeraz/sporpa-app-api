from typing import Any, Type

import pytest

from django.db import connection
from django.db.models.base import ModelBase
from django.utils import timezone

from utils.models import TrackingMixin

pytestmark = pytest.mark.django_db


@pytest.fixture(scope="module")
def TrackingMixinTestModel(django_db_blocker: Any) -> Type[TrackingMixin]:
    with django_db_blocker.unblock():
        model: Type[TrackingMixin] = ModelBase(  # type: ignore
            f"__TestModel__{TrackingMixin.__name__}",
            (TrackingMixin,),
            {
                "__module__": TrackingMixin.__module__,
            },
        )

        # Create the schema for the test model
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)  # type: ignore
        return model


class TestTrackingManagerMixin:
    def test_get_queryset_when_active_record(self, TrackingMixinTestModel: Type[TrackingMixin]) -> None:
        TrackingMixinTestModel.objects.create()
        assert TrackingMixinTestModel.objects.count() == 1
        assert TrackingMixinTestModel.all_objects.count() == 1

    def test_get_queryset_when_passive_record(self, TrackingMixinTestModel: Type[TrackingMixin]) -> None:
        TrackingMixinTestModel.objects.create(deleted_at=timezone.now())
        assert TrackingMixinTestModel.objects.count() == 0
        assert TrackingMixinTestModel.all_objects.count() == 1
