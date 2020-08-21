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
from django.contrib.auth.decorators import login_required






from .models import Article, Rubric, Comment
from .forms import ArticleForm, AIFormSet, UserRegForm, ChangeUserInfoForm, CommentForm




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

@staff_member_required
def article_change_staff(request, pk):
	article = get_object_or_404(Article, pk = pk)
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES, instance = article)
		if form.is_valid():
			article = form.save()
			formset = AIFormSet(request.POST, request.FILES, instance = article)
			if formset.is_valid():
				formset.save()
				messages.add_message(request, messages.SUCCESS, message = 'Статья изменена!')
				return redirect('main:home')
	else:
		form = ArticleForm(instance = article)
		formset = AIFormSet(instance = article)
	context = {'form':form, 'formset':formset}
	return render (request, 'main/article_change_staff.html', context)



from .forms import EditArticleForm
from .models import EditArticle
@login_required(login_url = '/user/login/')
def article_change_user(request, pk):
	article = get_object_or_404(Article, pk = pk)

	form_class = EditArticleForm
	if request.method == 'POST':
		e_form = form_class(request.POST)
		if e_form.is_valid():
			edit = EditArticle.objects.create(
				article = article,
				title = e_form.cleaned_data['title'],
				content = e_form.cleaned_data['content'],
				image = e_form.cleaned_data['image'])
			edit.save()
			messages.add_message(request, messages.SUCCESS, message = 'Спасибо за правки!')
			return redirect('main:home')
	else:
		form = EditArticleForm(instance = article)
		context = {'form':form}
		return render(request, 'main/article_change_user.html', context)


@staff_member_required
def article_delete(request, pk):
	article = get_object_or_404(Article, pk = pk)
	if request.method == 'POST':
		article.delete()
		messages.add_message(request, messages.SUCCESS, message = 'Статья удалена')
		return redirect('main:home')
	else:
		context = {'article':article}
		return render (request, 'main/article_delete.html', context)

@login_required(login_url = '/user/login/')
def article_detail(request, pk):
	article = Article.objects.get(pk = pk)
	ai = article.additionalimage_set.all()
	comment = Comment.objects.filter(article = pk)
	initial = {'article':article.pk}
	if request.user.is_authenticated:
		initial['author'] = request.user.username
	form_class = CommentForm
	form = form_class(initial = initial)
	if request.method == 'POST':
		c_form = form_class(request.POST)
		if c_form.is_valid():
			response = c_form.save()
			response.author = request.user.username
			response.save()
			messages.add_message(request, messages.SUCCESS, message = 'Комментарий успешно добавлен')
			return redirect('main:home')
		else:
			form = c_form
			messages.add_message(request, messages.WARNING, message = 'Комментарий не был добавлен')	
	context = {'article' : article, 'ai' : ai, 'comment':comment, 'form':form}
	return render(request, 'main/detail.html', context)



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

# views for comments
def comment_delete(request, pk):
	comment = get_object_or_404(Comment, pk = pk)
	if request.user.is_staff or request.user.username == comment.author:
		if request.method == 'POST':
			comment.delete()
			messages.add_message(request, messages.SUCCESS, message = 'Комментарий был удален!')
			return redirect('main:home')
		else:
			context = {'comment':comment}
			return render(request, 'main/comment_delete.html', context)
	else:
		raise Http404



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
