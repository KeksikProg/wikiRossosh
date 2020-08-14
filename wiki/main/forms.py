from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiField, Button, Field
from django.forms import inlineformset_factory, modelformset_factory
from django.forms.models import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

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

# for User
class UserRegForm(forms.ModelForm):
	email = forms.EmailField(
		required = True,
		label = 'Электронная почта')

	pass1 = forms.CharField(
		label = 'Пароль',
		widget = forms.PasswordInput,
		help_text = password_validation.password_validators_help_text_html())

	pass2 = forms.CharField(
		label = 'Повторите пароль',
		widget = forms.PasswordInput,
		help_text = password_validation.password_validators_help_text_html())

	def clean(self):
		passw1 = self.cleaned_data['pass1']
		if passw1:
			password_validation.validate_password(passw1)
		super().clean()
		passw2 = self.cleaned_data['pass2']
		if passw1 and passw2 and passw1 != passw2:
			errors = {'pass2' : ValidationError(
				'Введенные пароли не совпадают, попробуйте ещё раз',
				code = 'password_missmatch')}
			raise ValidationError(errors)

	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data['pass1'])
		if commit:
			user.save()
		return user

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('username', css_class = 'form-group col-md-6 mb-0'),
				Column('email', css_class = 'form-group col-md-4 mb-0'),
				css_class = 'form-row'),

			Row(
				Column('pass1', css_class = 'form-group col-md-4 mb-0'),
				Column('pass2', css_class = 'form-group col-md-4 mb-0'),
				css_class = 'form-row'),
			
			Row(
				Column('first_name', css_class = 'form-group col-md-4 mb-0'),
				Column('last_name', css_class = 'form-group col-md-4 mb-0'),
				css_class = 'form_row'),

			Submit('submit', 'Зарегистрироваться'))

	class Meta:
		model = User
		fields = ('username', 'email', 'pass1', 'pass2', 'first_name', 'last_name')	
