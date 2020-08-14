from django.urls import path


from .views import home, other, add_article, ALogin, ALogout, UserRegView

urlpatterns = [
	path('', home, name = 'home'), # урл которые показывает начальную страницу
	path('other/<str:page>', other, name = 'other'), # урл который будет выводить бумаги какие-то


	# Здесь будут все урл связанные с статьями
	path('article/add_article/', add_article, name = 'add_article'),

	# Здесь урлы связанные с действиями над пользователем
	path('user/login/', ALogin.as_view(), name = 'login'),
	path('user/logout/', ALogout.as_view(), name = 'logout'),

	# urls for register user
	path('user/register/', UserRegView.as_view(), name = 'register'),



]