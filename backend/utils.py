import json

from django.http import QueryDict
from rest_framework import parsers
from rest_framework.exceptions import NotFound
from rest_framework.serializers import ValidationError
from django.db import models


def validate_exist_and_return_array(validated_data: list, model: type[models.Model]) -> list[models.Model]:
    """
    Validate if the objects in validated_data exist in the specified model and return them.
    """
    if validated_data is None:
        return []
    ids = [obj.id for obj in validated_data]
    objects = model.objects.filter(id__in=ids)
    if len(ids) != len(objects):
        raise ValidationError({f'{model.__name__}': "One of the objects doesn't exist."})
    return objects


def validate_exist_and_return(validated_data, model: type[models.Model]) -> models.Model | None:
    if validated_data is None:
        return None
    try:
        obj = model.objects.get(id=validated_data.id)
    except model.DoesNotExist:
        raise NotFound({f'{model.__name__}': 'Object does not exist'})
    return obj


def convert_form_to_data(data: dict) -> dict:
    form_data = {
        **(json.loads(data['data']) if data.get('data') else {}),
        **({'audio': data['audio']} if data.get('audio') else {}),
        **({'picture': data['picture']} if data.get('picture') else {})
    }
    return form_data
