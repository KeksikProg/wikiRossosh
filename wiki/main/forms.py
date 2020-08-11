from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiField, Button, Field
from django.forms import inlineformset_factory, modelformset_factory
from django.forms.models import formset_factory
from django.contrib.auth.models import User

from .models import Article, AdditionalImage

# for articles
class ArticleForm(forms.ModelForm):
	# Я около 5 часов пытался сделать нормально вместе с наборами форм но у меня не получилось
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.helper = FormHelper()
	# 	self.helper.layout = Layout(
	# 		Row(
	# 			Column('title', css_class = 'form-group col-md-6 mb-0'),
	# 			Column('rubric', css_class = 'form-group col-md-4 mb-0'),
	# 			Column('street', css_class = 'form-group col-md-2 mb-0'),
	# 			css_class = 'form-row'),

	# 		'content',
	# 		'image',
			
	# 		)

	class Meta:
		model = Article
		fields = ('rubric','title','street','content','image')
		widgets = {'created_at' : forms.HiddenInput, 'street' : forms.TextInput(attrs = {'placeholder':'Ул: [Д: Кв: (если нужно)]'})}
AIFormSet = inlineformset_factory(Article, AdditionalImage, fields = '__all__')