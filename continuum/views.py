from django.shortcuts import render, get_object_or_404
from .forms import ProjectForm, VoteForm
from .models import Project, Vote

def index(request):
	return render(request, 'continuum/index.html')

def enterProject(request):
	form = ProjectForm(request.POST or None)
	if form.is_valid():
		vote = form.save(commit=False)
		form.save()
		return render(request, 'continuum/index.html')
	context = { 
			'form': form
			}
	return render(request, 'continuum/create_project.html', context)

def detailProject(request):
	projects = Project.objects.all()
	context = {
		'projects': projects
	}
	return render(request, 'continuum/view_projects.html', context)

def voteProject(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	form = VoteForm()
	contador = Vote.objects.filter(project_id=project_id)
	try: 
		if contador[0].suma <= 0:
			vote = Vote(form.project.data, 1)
			vote.save()
			return render(request, 'continuum/index.html')
		else:
			pass
	except:
		context = {
			'form': form
		}
		return render(request, 'continuum/cast_a_vote.html', context)
	context = {
		'form': form
	}
	return render(request, 'continuum/cast_a_vote.html', context)