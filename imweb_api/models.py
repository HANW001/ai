from django.db import models

# Create your models here.
class ImwebUser(models.Model):
    mall = models.CharField(primary_key=True, max_length=255)
    id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'imweb_user'