from django.db import models


class Persons(models.Model):
    class StatusChoices(models.TextChoices):
        ALIVE = "Alive"
        DEAD = "Dead"
        UNKNOWN = "unknown"

    class GenderChoices(models.TextChoices):
        FEMALE = "Female"
        MALE = "Male"
        GENDERLESS = "Genderless"
        UNKNOWN = "unknown"

    api_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=StatusChoices.choices)
    species = models.CharField(max_length=30)
    gender = models.CharField(max_length=20, choices=GenderChoices.choices)
    image = models.URLField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class TaskLog(models.Model):
    task_name = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_name} at {self.timestamp}"
