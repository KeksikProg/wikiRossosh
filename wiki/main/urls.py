from django.urls import path


from .views import home, other, add_article

urlpatterns = [
	path('', home, name = 'home'), # урл которые показывает начальную страницу
	path('other/<str:page>', other, name = 'other'), # урл который будет выводить бумаги какие-то


	# Здесь будут все урл связанные с статьями
	path('article/add_article/', add_article, name = 'add_article'),



]