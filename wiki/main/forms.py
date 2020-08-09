from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiField, LayoutObject
from django.forms import inlineformset_factory
from django.forms.models import formset_factory

from .models import Article, AdditionalImage


class ArticleForm(forms.ModelForm):
	

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('title', css_class = 'form-group col-md-6 mb-0'),
				Column('rubric', css_class = 'form-group col-md-4 mb-0'),
				Column('street', css_class = 'form-group col-md-2 mb-0'),
				css_class = 'form-row'),
			

			'content',
			'image',
			MultiField(
				Formset('formset')),

			Submit('submit', 'Sign in')
		)


	class Meta:
		model = Article
		fields = ('rubric','title','content','street','image')
		widgets = {'created_at' : forms.HiddenInput, 'street' : forms.TextInput(attrs = {'placeholder':'Ул: [Д: Кв: (если нужно)]'})}


AIFormSet = inlineformset_factory(Article, AdditionalImage, fields = '__all__')


