from django.contrib import admin

from .models import Article, Rubric, Comment

admin.site.register(Rubric)
admin.site.register(Article)

# Register your models here.
