from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout






from .models import Article, Rubric
from .forms import ArticleForm, AIFormSet, UserRegForm, ChangeUserInfoForm




# views у которых нет определенного разделения
def home(request):
	# будет выводить нлавную страницу
	articles = Article.objects.all()
	context = {'articles':articles}
	return render(request, 'main/home.html', context)

def other(request, page): 
	# Используется для того чтобы выводить документы различные (ну у меня будут не документы)
	try:
		template = get_template('main/' + page + '.html') # Пытаемся получить шаблон
	except TemplateDoesNotExist: # Если не находит такуб страницу
		raise Http404 # То ошибка 404 (страница не найдена)
	return HttpResponse(template.render(request = request))



# views связанные с статьями
@staff_member_required
def add_article(request):
	if request.method == 'POST':
		forms = ArticleForm(request.POST, request.FILES)
		if forms.is_valid():
			article = forms.save()
			formset = AIFormSet(request.POST, request.FILES, instance = article)
			if formset.is_valid():
				formset.save()
				messages.add_message(request, messages.SUCCESS, message = 'Статья успешно написана!')
				return redirect('main:home')
	else:
		forms = ArticleForm(initial = {})
		formset = AIFormSet()
	context = {'forms':forms, 'formset':formset}
	return render (request, 'main/add_article.html', context)

# views login and logout
class ALogin(LoginView):
	template_name = 'main/login.html'
class ALogout(LogoutView):
	template_name = 'main/logout.html'



# views for user
class UserRegView(CreateView):
	model = User
	template_name = 'main/register.html'
	form_class = UserRegForm
	success_url = reverse_lazy('main:login')

class ChangeUserInfo(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
	model = User
	template_name = 'main/change_user_info.html'
	form_class = ChangeUserInfoForm
	success_url = reverse_lazy('main:home')
	success_message = 'Личные данные пользователя были успешно изменены!'

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset = None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)

class ChangeUserPass(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
	template_name = 'main/change_pass.html'
	success_url = reverse_lazy('main:home')
	success_message = 'Пароль успешно изменен!'

class DeleteUserView(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
	model = User
	template_name = 'main/delete_user.html'
	success_url = reverse_lazy('main:home')

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logout(request)
		messages.add_message(request, messages.SUCCESS, message = 'Пользователь успешно удален!')
		return super().post(request, *args, **kwargs)

	def get_object(self, queryset = None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)





# views for password reset
class UserPassResetView(PasswordResetView):
	template_name = 'main/password_reset_form.html'
	subject_template_name = 'email/password_reset_subj.txt'
	email_template_name = 'email/password_reset_body.html'
	success_url = reverse_lazy('main:password_reset_done')

class UserPassResetDone(PasswordResetDoneView):
	template_name = 'main/password_reset_done.html'

class UserPassResetConfirmView(PasswordResetConfirmView):
	template_name = 'main/password_reset_confirm.html'
	success_url = reverse_lazy('main:login')





# Create your views here.
