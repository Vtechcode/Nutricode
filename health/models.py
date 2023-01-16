from django.db import models

# Create your models here.
class DiseaseSearch(models.Model):
    disease_name = models.CharField(max_length=500)
    disease_symptoms = models.TextField(null=True, blank=True)
    disease_diet = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'DiseaseSearches'