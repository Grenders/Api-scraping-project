import random

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from persons.models import Persons
from persons.serializers import PersonSerializers


@api_view(["GET"])
@extend_schema(responses=PersonSerializers)
def get_persons(request: Request) -> Response:
    pks = Persons.objects.values_list("pk", flat=True)
    if not pks:
        return Response({"error": "Not found Person"}, status=status.HTTP_404_NOT_FOUND)
    random_pk = random.choice(pks)
    random_person = Persons.objects.get(pk=random_pk)
    serializer = PersonSerializers(random_person)
    return Response(serializer.data, status=status.HTTP_200_OK)


class PersonListView(generics.ListAPIView):
    serializer_class = PersonSerializers
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Persons.objects.all().order_by("id")

        name = self.request.query_params.get("name")
        species = self.request.query_params.get("species")

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if species is not None:
            queryset = queryset.filter(species__icontains=species)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name", description="Filter by name ", required=False, type=str
            ),
            OpenApiParameter(
                name="species",
                description="Filter by species ",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="page",
                description="Page number for pagination",
                required=False,
                type=int,
            ),
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:
        """List person with filer by name"""
        return super().get(request, *args, **kwargs)
