from django.shortcuts import render

from .models import Article, Rubric

def home(request):
	articles = Article.objects.all()
	context = {'articles':articles}
	return render(request, 'main/home.html', context)

# Create your views here.
