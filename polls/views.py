from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Poll, Choice, Vote
from authentication.models import User


def all_polls(request):
    if not request.user.is_authenticated:
        return redirect('/')

    all_polls = Poll.objects.all()

    return render(request, 'polls/all_polls.html', {
        'polls': all_polls
    })


def poll(request, poll_id):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        poll = Poll.objects.get(pk=poll_id)
        choices = poll.choices.all()

        user = User.objects.get(auth_user=request.user)
        old_votes = Vote.objects.filter(user=user, poll=poll)

        return render(request, 'polls/poll.html', {
            'poll': poll,
            'choices': choices,
            'old_votes': old_votes
        })
    elif request.method == 'POST':
        request_body = dict(request.POST)

        choice_id = request_body.get('choice')[0]

        choice = Choice.objects.get(pk=choice_id)
        user = User.objects.get(auth_user=request.user)

        Vote.objects.filter(user=user, poll=choice.poll).delete()

        new_vote = Vote(
            poll=choice.poll,
            choice=choice,
            user=user
        )
        new_vote.save()

        return redirect('/polls')


def poll_results(request, poll_id):
    if not request.user.is_authenticated:
        return redirect('/')

    poll = Poll.objects.get(pk=poll_id)
    choices = Choice.objects.filter(poll=poll)

    choices_votes = [{
        'choice': choice,
        'votes': choice.votes.all()
    } for choice in choices]

    return render(request, 'polls/poll_results.html', {
        'poll': poll,
        'choices_votes': choices_votes
    })


def create_poll(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'polls/create_poll.html')
    elif request.method == 'POST':
        request_body = dict(request.POST)

        question = request_body.get('question')[0]
        choices_texts = request_body.get('choice')
        choices_texts = [choice_text for choice_text in choices_texts if choice_text != '']

        if question == '':
            return render(request, 'polls/create_poll.html', {
                'error': 'Question text must not be empty'
            })
        elif len(choices_texts) < 2:
            return render(request, 'polls/create_poll.html', {
                'error': 'Poll must have at least 2 choices'
            })

        new_poll = Poll(
            text=question
        )
        new_poll.save()

        for choice_text in choices_texts:
            new_choice = Choice(
                text=choice_text,
                poll=new_poll
            )
            new_choice.save()

        return redirect('/')
