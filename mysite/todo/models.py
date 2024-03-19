from django.db import models

# Create your models here.
class Todo(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField(null=True)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"