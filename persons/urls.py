from django.urls import path

from persons.views import get_persons, PersonListView

app_name = "persons"

urlpatterns = [
    path("persons/random/", get_persons, name="random-person"),
    path("persons/", PersonListView.as_view(), name="person-list"),
]
