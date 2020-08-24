from django.contrib import admin
from django.urls import reverse

from .models import Article, Rubric, Comment, AdditionalImage, EditArticle



class AddImageInline(admin.TabularInline):
	model = AdditionalImage
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('rubric', 'title', 'street', 'created_at') # Что будет видно об объекте в общем списке объектов
	list_filter = ('rubric',) # По каким полям можно будет произвести фильтрация
	search_fields = ('title',)
	readonly_fields = ('created_at',)
	inlines = (AddImageInline,)

	fieldsets = ( 
		# Этот сет делает более красивым детальное рассмотрение объекта
		(None, {
			'fields' : (('title', 'rubric'), 'content'),
			'classes':('wide',)
			}),
		('Дополнительная информация', {
			'fields':('street', 'image'),
			'classes':('collapse',),
			'description':'Поля необязательные для заполнения',}))



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('article', 'author', 'created_at')
	search_fields = ('article',)
	fields = (('article', 'author'), 'content')
	readonly_fields = ('created_at',)



@admin.register(EditArticle)
class EditArticleAdmin(admin.ModelAdmin):
	list_display = ('article',)
	search_fields = ('article',)
	fields = ('title', 'content', 'image')





admin.site.register(Rubric)
admin.site.register(AdditionalImage)


admin.site.site_title = 'Администрирование'
admin.site.site_header = 'Администрация сайта РоссошьWiki'
admin.site.index_title = 'Каталоги'

# Register your models here.
