from django.db import models
from .util import get_timestamp_path

'''Модели для статей, дополнительных фотографий и модели для редактирования статей'''
class Rubric(models.Model):
	'''Модель для рубрик'''
	name = models.CharField(
		max_length = 30,
		db_index = True,
		unique = True,
		verbose_name = 'Название')
	
	order = models.SmallIntegerField(
		default = 0,
		db_index = True, 
		verbose_name = 'Порядок')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Рубрика'
		verbose_name_plural = 'Рубрики'

class Article(models.Model):
	rubric = models.ForeignKey(
		Rubric,
		on_delete = models.PROTECT,
		verbose_name = 'Рубрика')

	title = models.CharField(
		max_length = 50,
		verbose_name = 'Название',)

	content = models.TextField(
		verbose_name = 'Описание',)

	street = models.CharField(
		blank = True,
		max_length = 100,
		verbose_name = 'Местоположение')

	image = models.ImageField(
		blank = True,
		upload_to = get_timestamp_path,
		verbose_name = 'Фотография')

	created_at = models.DateTimeField(
		auto_now_add = True,
		db_index = True,
		verbose_name = 'Добавлено')

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		for ai in self.additionalimage_set.all():
			ai.delete()
		super().delete(*args, **kwargs)

	class Meta:
		verbose_name = 'Статья'
		verbose_name_plural = 'Статьи'
		ordering = ['-created_at']
class AdditionalImage(models.Model):
	article = models.ForeignKey(
		Article,
		on_delete = models.CASCADE,
		verbose_name = 'Дополнительные фотографии')
	image = models.ImageField(
		upload_to = get_timestamp_path,
		verbose_name = 'Фотография',)
class EditArticle(models.Model):
	article = models.ForeignKey(
		Article,
		on_delete = models.CASCADE,
		verbose_name = 'Статья')

	title = models.CharField(
		max_length = 50,
		verbose_name = 'Название',)

	content = models.TextField(
		verbose_name = 'Описание',)

	image = models.ImageField(
		blank = True,
		upload_to = get_timestamp_path,
		verbose_name = 'Фотография')

	class Meta:
		verbose_name = 'Правка'
		verbose_name_plural = 'Правки'

'''Модели для комментариев'''
class Comment(models.Model):
	article = models.ForeignKey(
		Article,
		on_delete = models.CASCADE,)

	author = models.CharField(
		max_length = 40,
		verbose_name = 'Автор')

	content = models.TextField(
		verbose_name = 'Содержание')

	created_at = models.DateTimeField(
		auto_now_add = True,
		db_index = True,
		verbose_name = 'Добавлено')

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комметарии'







# Create your models here.
