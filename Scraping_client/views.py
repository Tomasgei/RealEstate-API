from django.shortcuts import render,HttpResponse
from django.urls import reverse
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView , UpdateAPIView, CreateAPIView
from Scraping_client.models import Project,Property , PropertyHistory
from Scraping_client.serializers import ProjectSerializer, ApartmentSerializer, PropHistorySerializer

# Create your views here.

class ProjectsListAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectsCreateAPIView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectsDetailAPIView(RetrieveAPIView):
    lookup_field = "pk"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectsUpdateAPIView(UpdateAPIView):
    lookup_field = "pk"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectsDestroyAPIView(DestroyAPIView):
    lookup_field = "pk"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer



class ApartmentsListAPIView(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = ApartmentSerializer

#///////////////////////////////////////////
## Property actual 
#///////////////////////////////////////////
# create single
class PropertyCreateAPIView(CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = ApartmentSerializer

# retrieve single
class PropertyDetailAPIView(RetrieveAPIView):
    lookup_field = "pk"
    queryset = Property.objects.all()
    serializer_class = ApartmentSerializer

# update single
class PropertyUpdateAPIView(UpdateAPIView):
    lookup_field = "pk"
    queryset = Property.objects.all()
    serializer_class = ApartmentSerializer

# destroy single
class PropertyDestroyAPIView(DestroyAPIView):
    lookup_field = "pk"
    queryset = Property.objects.all()
    serializer_class = ApartmentSerializer

#///////////////////////////////////////////
## Property history 
#///////////////////////////////////////////
PropHistorySerializer

# create single
class PropHistoryCreateAPIView(CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropHistorySerializer

# retrieve single
class PropHistoryDetailAPIView(RetrieveAPIView):
    lookup_field = "pk"
    queryset = PropertyHistory.objects.all()
    serializer_class = PropHistorySerializer

# update single
class PropHistoryUpdateAPIView(UpdateAPIView):
    lookup_field = "pk"
    queryset = PropertyHistory.objects.all()
    serializer_class = PropHistorySerializer

# destroy single
class PropHistoryDestroyAPIView(DestroyAPIView):
    lookup_field = "pk"
    queryset = PropertyHistory.objects.all()
    serializer_class = PropHistorySerializer