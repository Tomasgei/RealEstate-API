from django.db import models
from django.db.models.base import Model

# Create your models here.

class Project(models.Model):
    
    UpdateDate = models.CharField(max_length= 50)
    ProjectId = models.CharField(max_length= 20, primary_key=True)
    

    def __str__(self):
        return str(self.ProjectId) 
    

class Property(models.Model):
    """
    This model tracks actual state of all property listings
    """
    index = models.IntegerField(primary_key=True )
    updateDate = models.DateField()
    flatNumber = models.CharField(max_length=10)
    roomsNumber = models.IntegerField(null=True)
    floorsNumber = models.IntegerField(null=True)
    flatArea = models.FloatField()
    balconyTerraceArea = models.FloatField(null=True)
    totalArea = models.FloatField(null=True)
    salesPrice = models.FloatField(null=True)
    propStatus = models.CharField(max_length=20)

    
    def __str__(self):
        return str(self.flatNumber) 


class PropertyHistory(models.Model):
    """
    This model tracks historical state of property
    """
    
    updateDate = models.DateField()
    flatNumber = models.ForeignKey(Property,on_delete=models.CASCADE)
    propStatus = models.CharField(max_length=20)
        
    def __str__(self):
        return str(self.flatNumber)
