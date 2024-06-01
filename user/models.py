from django.db import models

class Cafe24User(models.Model):
    mall = models.CharField(max_length=255)
    id = models.CharField(primary_key=True, max_length=45)
    password = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secretkey = models.CharField(max_length=255)
    servicekey = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'cafe24_user'


class ImwebUser(models.Model):
    mall = models.CharField(primary_key=True, max_length=255)
    id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'imweb_user'