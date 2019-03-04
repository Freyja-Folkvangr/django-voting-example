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
            # 1: remove spaces.
            # 2: convert to list separated by comma.
            # 3: remove duplicates
            # 4: convert each to int.
            # 5: convert map obj to list
            the_vote = list(map(int, dict.fromkeys(vote.votes.replace(' ', '').split(','))))
            if len(the_vote) != len(valid_choice_ids):
                return render(request, 'continuum/index.html', {
                    'error_message': 'Your vote length is {} and it should be {}. Please include all choices in your vote ordered by priority. Consider that duplicates are removed automatically.'.format(
                        len(the_vote), len(valid_choice_ids))})
            for item in the_vote:
                if item in valid_choice_ids:
                    pass
                else:
                    return render(request, 'continuum/index.html', {
                        'error_message': 'Invalid vote....... The format may be incorrect or the choices does not belongs to the selected voting process. HINT: process: {}. your vote: {}. valid votes {}'.format(
                            vote.process.id, the_vote, valid_choice_ids)})
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
    votes = Votes.objects.filter(process_id=question_id)
    choices = Choice.objects.filter(question_id=question.id)
    choice_list = {}
    for choice in choices: choice_list[str(choice.id)] = {'id': choice.id, 'votes': 0, 'cost': choice.cost,
                                                          'name': choice.choice_text}
    rounds = {}
    # create dict structure
    for i in range(0, len(choice_list)):
        rounds[str(i)] = []
    results = []
    expenses = 0
    # rounds of voting
    for i in range(0, len(choice_list)):
        try:
            for vote in votes:
                # sum the vote to the 'choice'
                choice_list[str(vote.get_vote_list()[i])]['votes'] += 1
                # add the vote to the round
                rounds[str(i)].append(vote.get_vote_list()[i])
            # sort dict by greatest number of votes
            round = sorted(choice_list, key=lambda x: choice_list[x]['votes'])[::-1]
            for item in round:
                # check budget
                tmp = expenses + choice_list[item]['cost']
                if (question.budget - tmp >= 0):
                    expenses += choice_list[item]['cost']
                    # we have a winner, add it to results and delete from choice list, proceed with next round
                    results.append(choice_list[item])
                    del choice_list[item]
                    break
                else:
                    # winner choice not in budget, delete from choice list and proceed
                    del choice_list[item]
        except KeyError: pass
    print(expenses)
    print(results)
    print(rounds)
    debug = []
    for item in list(rounds):
        debug.append(''.join(str(e) + ' ' for e in rounds[item]))
    context = {
        'results': results,
        'rounds': rounds,
        'debug': debug,
        'expenses': expenses,
        'question': question
    }
    return render(request, 'continuum/results.html', context)
