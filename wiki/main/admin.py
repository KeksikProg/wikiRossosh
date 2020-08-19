from django.contrib import admin

from .models import Article, Rubric, Comment, AdditionalImage

admin.site.register(Rubric)
admin.site.register(Article)
admin.site.register(AdditionalImage)

# Register your models here.
