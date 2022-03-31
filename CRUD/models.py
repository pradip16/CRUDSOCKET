from django.db import models

# Create your models here.
class CRUD_OPR(models.Model):
    Name = models.CharField(max_length=100)
    Email= models.EmailField()
    Password = models.CharField(max_length=200)


    def __str__(self) -> str:
        return self.Name