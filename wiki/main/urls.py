from django.urls import path
from .views import home

urlpatterns = [
	path('', home, name = 'home'), # урл которые показывает начальную страницу
]