from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *
from django.urls import reverse


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    context = {
        'voting_processes': latest_question_list
    }
    print(context)
    return render(request, 'continuum/index.html', context)


def create_choice(request):
    form = create_choice_form(request.POST or None)
    processes = Question.objects.all().count()
    if form.is_valid():
        vote = form.save(commit=False)
        form.save()
        return render(request, 'continuum/create_choice.html')
    context = {
        'form': form,
        'voting_process': processes
    }
    return render(request, 'continuum/create_choice.html', context)


def create_question(request):
    form = create_question_form(request.POST or None)
    processes = Question.objects.all().count()
    context = {
        'form': form,
        'number_of_processes': processes
    }
    if form.is_valid():
        form.save()
        return render(request, 'continuum/index.html', context)
    return render(request, 'continuum/create_voting_process.html', context)


def view_choices(request):
    choices = Choice.objects.all()
    context = {
        'choices': choices
    }
    return render(request, 'continuum/view_choices.html', context)


def view_choice_details(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    return render(request, 'continuum/view_choice_details.html', {'choice': choice})


def submitVote(request):
    form = vote_form(request.POST or None)
    if form.is_valid():
        vote = form.save(commit=True)
        form.save()
        votes = Votes(name=request.form.name, vote=request.form.vote)
        return render(request, 'continuum/index.html')

    context = {
        'form': form
    }
    return render(request, 'continuum/cast_a_vote.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'continuum/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'continuum/view_choices.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
