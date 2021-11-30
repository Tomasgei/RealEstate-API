
from django.db.models import fields
from rest_framework import serializers
from Scraping_client.models import Project, Property, PropertyHistory


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("UpdateDate","ProjectId")
    
class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
                'index',
                'flatNumber',
                'roomsNumber',
                'floorsNumber',
                'flatArea',
                'balconyTerraceArea',
                'totalArea',
                'salesPrice',
                'propStatus',
                'updateDate'
                )
                
class PropHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyHistory
        fields = (
                "id",
                "updateDate",
                "propStatus",
                "flatNumber_id"
                )