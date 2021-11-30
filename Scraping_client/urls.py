
from django.urls import path, include
from . import views

views.PropertyDetailAPIView
urlpatterns = [
    path('',views.ProjectsListAPIView.as_view(), name= "home" ),
    path('project/',views.ProjectsListAPIView.as_view(), name= "project" ),
    path('project/<str:pk>',views.ProjectsDetailAPIView.as_view(), name= "project_detail" ),
    path('project/create/',views.ProjectsCreateAPIView.as_view(), name= "project_create" ),
    path('project/delete/<str:pk>',views.ProjectsDestroyAPIView.as_view(), name= "project_detail_delete" ),
    path('project/update/<str:pk>',views.ProjectsUpdateAPIView.as_view(), name= "project_detail_update" ),

    path('property/',views.ApartmentsListAPIView.as_view(), name= "property_all" ),
    path('property/<int:pk>',views.PropertyDetailAPIView.as_view(), name= "property_detail" ),
    path('property/create/',views.PropertyCreateAPIView.as_view(), name= "property_create" ),
    path('property/delete/<int:pk>',views.PropertyDestroyAPIView.as_view(), name= "property_detail_delete" ),
    path('property/update/<int:pk>',views.PropertyUpdateAPIView.as_view(), name= "property_detail_update" ),
    
    path('property-history/',views.ApartmentsListAPIView.as_view(), name= "property-hist_all" ),

    path('property-history/<int:pk>',views.PropHistoryDetailAPIView.as_view(), name= "property-hist_detail" ),
    path('property-history/create/',views.PropHistoryCreateAPIView.as_view(), name= "property-hist_create" ),
    path('property-history/delete/<int:pk>',views.PropHistoryDestroyAPIView.as_view(), name= "property-hist_detail_delete" ),
    path('property-history/update/<int:pk>',views.PropHistoryUpdateAPIView.as_view(), name= "property-hist_detail_update" ),
]

