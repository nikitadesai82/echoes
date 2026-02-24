from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('birds/', views.birds_list, name='birds_list'),
    path('birds/<slug:slug>/', views.bird_detail, name='bird_detail'),  
    path('flora_list/', views.flora_list, name='flora_list'),
    path('flora/<int:flora_id>/', views.flora_detail, name='flora_detail'),
    path("Deepdive/", views.Deepdive, name="Deepdive"),
    path("Birdwatching/", views.Birdwatching, name="Birdwatching"),
    path("Naturetrail/", views.Naturetrail, name="Naturetrail"),
    path("Urbanlegends/",views.Urbanlegends, name="Urbanlegends"),
    path("Gallery/",views.Gallery,name="Gallery"),
    path('gallery/bird/<int:bird_id>/', views.bird_gallery, name='bird_gallery'),
    path('gallery/flora/<int:flora_id>/', views.flora_gallery, name='flora_gallery'),
    path("MDGallery/",views.MDGallery,name="MDGallery"),
    path("Credits/",views.Credits,name="Credits"),
		path("Disclaimer/",views.Disclaimer,name="Disclaimer"),
		path("Privacy/",views.Privacy,name="Privacy"),
		path("Terms/",views.Terms,name="Terms"),
    path("__exit_kiosk__/", views.exit_kiosk, name="exit_kiosk"),


]