from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category_slug>/', views.category_detail_view, name='category_detail'),
]
