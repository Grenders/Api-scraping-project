from django.db import IntegrityError

from config import settings
from persons.models import Persons
import requests


def scraper() -> list[Persons]:
    next_url_to_scrape = settings.URL_FOR_SCRAPING

    persons = []
    while next_url_to_scrape is not None:
        response = requests.get(next_url_to_scrape)
        if response.status_code != 200:
            return persons
        person_response = response.json()

        for person_dict in person_response["results"]:
            try:
                persons.append(
                    Persons(
                        api_id=person_dict["id"],
                        name=person_dict["name"],
                        status=person_dict["status"],
                        species=person_dict["species"],
                        gender=person_dict["gender"],
                        image=person_dict["image"],
                    )
                )
            except KeyError as e:
                print(f"KeyError for person {person_dict.get('name', 'unknown')}: {e}")
        next_url_to_scrape = person_response["info"]["next"]
    return persons


def save_person(persons: list[Persons]) -> None:
    for person in persons:
        try:
            person.full_clean()
            person.save()
        except IntegrityError:
            print(f"Person with 'api_id' {person.api_id} already exist in DB")


def sync_person_api() -> None:
    persons = scraper()
    save_person(persons)
