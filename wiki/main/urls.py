from django.urls import path


from .views import home, other, add_article, ALogin, ALogout, UserRegView
from .views import UserPassResetView, UserPassResetDone, UserPassResetConfirmView
from .views import ChangeUserInfo, ChangeUserPass, DeleteUserView


urlpatterns = [



	# urls home amd other
	path('', home, name = 'home'), # урл которые показывает начальную страницу
	path('other/<str:page>/', other, name = 'other'), # урл который будет выводить бумаги какие-то



	# urls for articles
	path('article/add_article/', add_article, name = 'add_article'),



	# urls for users
	path('user/login/', ALogin.as_view(), name = 'login'),
	path('user/logout/', ALogout.as_view(), name = 'logout'),
	path('user/change_user_info/', ChangeUserInfo.as_view(), name = 'changeuserinfo'),
	path('user/chang_euser_pass/', ChangeUserPass.as_view(), name = 'changeuserpass'),
	path('user/delete_user/', DeleteUserView.as_view(), name ='deleteuser'),


	# urls for register user
	path('user/register/', UserRegView.as_view(), name = 'register'),



	# urls for password reset
	path('profile/password_reset_form/', UserPassResetView.as_view(), name = 'password_reset_form'),
	path('profile/password_reset_done/', UserPassResetDone.as_view(), name = 'password_reset_done' ),
	path('profile/password_reset_confirm/<uidb64>/<token>/', UserPassResetConfirmView.as_view(), name = 'password_reset_confirm'),




]