from django.db import models

class StaticPage(models.Model):
    slug = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
