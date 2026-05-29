from django.db import models
from django.conf import settings


MAX_SKILL_NAME_LENGTH = 124
MAX_PROJECT_NAME_LENGTH = 200
STATUS_MAX_LENGTH = 6


class Skill(models.Model):
    name = models.CharField(max_length=MAX_SKILL_NAME_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Открыт'),
        (STATUS_CLOSED, 'Закрыт'),
    ]

    name = models.CharField(max_length=MAX_PROJECT_NAME_LENGTH)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects'
    )
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='projects'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
