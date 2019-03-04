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
    return render(request, 'continuum/index.html', context)


def create_choice(request):
    form = create_choice_form(request.POST or None)
    processes = Question.objects.all().count()
    if form.is_valid():
        vote = form.save(commit=False)
        form.save()
        return render(request, 'continuum/index.html', {'message': 'Choice created!'})
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
        context['message'] = 'Voting process created!'
        return render(request, 'continuum/index.html', context)
    return render(request, 'continuum/create_voting_process.html', context)


def view_choices(request):
    choices = Choice.objects.all()
    count = Choice.objects.all().count()
    context = {
        'choices': choices,
        'count': count
    }
    return render(request, 'continuum/view_choices.html', context)


def view_choice_details(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    return render(request, 'continuum/view_choice_details.html', {'choice': choice})


def cast_a_vote(request):
    form = vote_form(request.POST or None)
    if form.is_valid():
        vote = form.save(commit=False)
        valid_choices = Choice.objects.filter(question_id=vote.process.id)
        valid_choice_ids = []
        for item in valid_choices:
            valid_choice_ids.append(item.id)
        try:
            #1: remove spaces. 2: convert to list separated by comma. 3: convert each to int. 4: convert map obj to list
            the_vote = list(map(int, vote.votes.replace(' ', '').split(',')))
            for item in the_vote:
                if item in valid_choice_ids:
                    pass
                else:
                    return render(request, 'continuum/index.html', {
                        'error_message': 'Invalid vote....... The format may be incorrect or the choices does not belongs to the selected voting process. HINT: process: {}. your vote: {}. valid votes {}'.format(vote.process.id, the_vote, valid_choice_ids)})
            form.save()
            return render(request, 'continuum/index.html', {'message': 'Vote submited!'})
        except:
            render(request, 'continuum/index.html', {
                'error_message': 'Invalid vote.......<br>The format may be incorrect or the choices does not belongs to the selected voting process'})

    context = {
        'form': form
    }
    return render(request, 'continuum/cast_a_vote.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'continuum/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'continuum/results.html', {'question': question})
