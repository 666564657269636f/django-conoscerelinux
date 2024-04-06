from django.db import models
from django.urls import reverse


class StaticPage(models.Model):
    slug = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("static-page", kwargs={"slug": self.slug})
