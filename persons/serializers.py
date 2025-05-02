from rest_framework import serializers

from persons.models import Persons


class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Persons
        fields = ("id", "api_id", "name", "status", "species", "gender", "image")
