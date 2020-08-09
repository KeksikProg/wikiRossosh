from .models import Rubric

def rubric_context_proccessor(request):
	context = {}
	context['rubrics'] = Rubric.objects.all()
	return context
