from django.contrib import admin
from . models import Project,Property,PropertyHistory

# Register your models here.
admin.site.register(Project)
admin.site.register(Property)
admin.site.register(PropertyHistory)