from django.db import models

class Datastore(models.Model):
    name=models.CharField(max_length=10)
    password=models.CharField(max_length=50)
    
