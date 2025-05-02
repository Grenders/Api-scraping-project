from django.test import TestCase, RequestFactory
from rest_framework import status
from unittest.mock import patch, Mock
from persons.models import Persons, TaskLog
from persons.scraper import scraper, save_person
from persons.views import get_persons, PersonListView

from datetime import datetime


class PersonsModelTests(TestCase):
    def test_create_person(self):
        person = Persons.objects.create(
            api_id=1,
            name="Rick Sanchez",
            status=Persons.StatusChoices.ALIVE,
            species="Human",
            gender=Persons.GenderChoices.MALE,
            image="https://example.com/rick.jpg",
        )
        self.assertEqual(person.name, "Rick Sanchez")
        self.assertEqual(str(person), "Rick Sanchez")

    def test_task_log_creation(self):
        task_log = TaskLog.objects.create(
            task_name="Sync API hourly", message="Test log"
        )
        self.assertEqual(task_log.task_name, "Sync API hourly")
        self.assertTrue(isinstance(task_log.timestamp, datetime))
        self.assertEqual(str(task_log), f"Sync API hourly at {task_log.timestamp}")


class ScraperTests(TestCase):
    @patch("persons.scraper.requests.get")
    def test_scraper_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "info": {"next": None},
            "results": [
                {
                    "id": 1,
                    "name": "Rick Sanchez",
                    "status": "Alive",
                    "species": "Human",
                    "gender": "Male",
                    "image": "https://example.com/rick.jpg",
                }
            ],
        }
        mock_get.return_value = mock_response

        persons = scraper()
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0].name, "Rick Sanchez")
        self.assertEqual(persons[0].api_id, 1)

    @patch("persons.scraper.requests.get")
    def test_scraper_non_200_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        persons = scraper()
        self.assertEqual(len(persons), 0)

    @patch("persons.scraper.requests.get")
    def test_scraper_key_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "info": {"next": None},
            "results": [
                {
                    "id": 1,
                    # Missing 'name' to trigger KeyError
                    "status": "Alive",
                    "species": "Human",
                    "gender": "Male",
                    "image": "https://example.com/rick.jpg",
                }
            ],
        }
        mock_get.return_value = mock_response

        with patch("builtins.print") as mocked_print:
            persons = scraper()
            self.assertEqual(len(persons), 0)
            mocked_print.assert_called_with("KeyError for person unknown: 'name'")

    def test_save_person(self):
        person = Persons(
            api_id=1,
            name="Rick Sanchez",
            status=Persons.StatusChoices.ALIVE,
            species="Human",
            gender=Persons.GenderChoices.MALE,
            image="https://example.com/rick.jpg",
        )
        save_person([person])
        saved_person = Persons.objects.get(api_id=1)
        self.assertEqual(saved_person.name, "Rick Sanchez")


class ViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.person = Persons.objects.create(
            api_id=1,
            name="Rick Sanchez",
            status=Persons.StatusChoices.ALIVE,
            species="Human",
            gender=Persons.GenderChoices.MALE,
            image="https://example.com/rick.jpg",
        )

    def test_get_persons(self):
        request = self.factory.get("/api/persons/")
        response = get_persons(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Rick Sanchez")

    def test_get_persons_not_found(self):
        Persons.objects.all().delete()
        request = self.factory.get("/api/persons/")
        response = get_persons(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Not found Person"})

    def test_person_list_view_filter_name(self):
        Persons.objects.create(
            api_id=2,
            name="Morty Smith",
            status=Persons.StatusChoices.ALIVE,
            species="Human",
            gender=Persons.GenderChoices.MALE,
            image="https://example.com/morty.jpg",
        )
        request = self.factory.get("/api/persons/list/?name=Rick")
        view = PersonListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Rick Sanchez")

    def test_person_list_view_filter_species(self):
        request = self.factory.get("/api/persons/list/?species=Human")
        view = PersonListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["species"], "Human")

    def test_person_list_view_pagination(self):
        for i in range(15):
            Persons.objects.create(
                api_id=i + 2,
                name=f"Person {i}",
                status=Persons.StatusChoices.ALIVE,
                species="Human",
                gender=Persons.GenderChoices.MALE,
                image=f"https://example.com/person{i}.jpg",
            )
        request = self.factory.get("/api/persons/list/?page=1")
        view = PersonListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
        self.assertTrue("count" in response.data)
        self.assertEqual(response.data["count"], 16)
