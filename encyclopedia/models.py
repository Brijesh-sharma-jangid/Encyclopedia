from django.db import models

class Data(models.Model):
    title = models.CharField(max_length=50,primary_key=True)
    body = models.TextField()

    def __str__(self):
        return f"{self.title}"