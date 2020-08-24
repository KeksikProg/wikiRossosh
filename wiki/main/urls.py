from django.urls import path


from .views import home, other, add_article, ALogin, ALogout, UserRegView
from .views import UserPassResetView, UserPassResetDone, UserPassResetConfirmView
from .views import ChangeUserInfo, ChangeUserPass, DeleteUserView, article_change_staff, article_delete
from .views import article_detail, comment_delete, article_change_user, edit_list


urlpatterns = [



	# urls home amd other
	path('', home, name = 'home'), # урл которые показывает начальную страницу
	path('other/<str:page>/', other, name = 'other'), # урл который будет выводить бумаги какие-то



	# urls for articles
	path('article/add_article/', add_article, name = 'add_article'),
	path('article/article_change_staff/<int:pk>/', article_change_staff, name = 'change_staff'),
	path('article/article_change_user/<int:pk>/', article_change_user, name = 'article_change_user'),
	path('article/article_delete/<int:pk>/', article_delete, name = 'article_delete'),
	path('article/detail/<int:pk>/', article_detail, name = 'article_detail'),



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

	# urls for comments
	path('article/comments/delete/<int:pk>', comment_delete, name = 'comment_delete'),

	# urls for edit article
	path('article/edit_list/<int:pk>', edit_list, name = 'edit_list'),




]