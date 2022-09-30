from django.db import models

# Create your models here.
class DiseaseSearch(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'DiseaseSearches'