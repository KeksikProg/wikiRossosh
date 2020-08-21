from django.contrib import admin

from .models import Article, Rubric, Comment, AdditionalImage, EditArticle

admin.site.register(Rubric)
admin.site.register(Article)
admin.site.register(AdditionalImage)
admin.site.register(EditArticle)

# Register your models here.
