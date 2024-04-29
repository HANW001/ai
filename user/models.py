from django.db import models

class User(models.Model):
    mall = models.CharField(null=False,max_length=255)
    id = models.AutoField(primary_key=True,null=False)
    password = models.CharField(null=False,max_length=255)
    client_id = models.CharField(null=False,max_length=255)
    client_secretkey = models.CharField(null=False,max_length=255)
    servicekey = models.CharField(null=False,max_length=255)