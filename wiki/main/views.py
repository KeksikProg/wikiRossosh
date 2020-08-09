from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect

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
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save()
			formset = AIFormSet(request.POST, request.FILES, instance = article)
			if formset.is_valid():
				formset.save()
				messages.add_message(request, messages.SUCCESS, message = 'Статья успешно написана!')
				return redirect('main:home')
	else:
		form = ArticleForm(initial = {})
		formset = AIFormSet()
	context = {'form':form, 'formset':formset}
	return render (request, 'main/add_article.html', context)





# Create your views here.
