from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from .models import Article, Rubric
from .forms import ArticleForm, AIFormSet


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

# views действия с пользователями

class ALogin(LoginView):
	template_name = 'main/login.html'
class ALogout(LogoutView):
	template_name = 'main/logout.html'





# Create your views here.
