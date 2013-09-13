from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.mail import mail_managers, EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView, FormView

from datetime import datetime

from .forms import EntryForm
from .models import Contest, Entry, Vote
from .utils import process_contest_entry


class ContestTemplateView(TemplateView):
    """
    This view does some initial construction to pull either the supplied contest
    or the base contest.
    """
    template_name = ''

    def dispatch(self, request, *args, **kwargs):

        try:
            # We need to figure out which contest is currently running.
            contest = Contest.objects.get(pk=kwargs.get('contest_id', 1))

        except Contest.DoesNotExist:
            return redirect('home')

        kwargs['contest'] = contest

        return super(ContestTemplateView, self).dispatch(request, *args, **kwargs)


class ContestEntriesView(ContestTemplateView):
    template_name = 'contest/entries.html'

    def get_context_data(self, **kwargs):

        contest = kwargs.get('contest')

        return {
            'contest': contest,
            'entries': contest.entries.filter(is_visible=True).order_by('-vote_count')
        }


class AddEntryView(ContestTemplateView, FormView):
    success_url = '/contest/thanks'
    form_class = EntryForm
    template_name = 'contest/submit_entry.html'

    def get(self, request, *args, **kwargs):
        """
        We have to add the contest to the context here.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['contest'] = kwargs.get('contest')

        return self.render_to_response(context)

    def form_valid(self, form):

        # TODO: Let's create a contest entry.

        # But for now, let's just process it.  This sends out some emails.
        process_contest_entry(form)

        return super(AddEntryView, self).form_valid(form)


class AddEntryThanksView(ContestTemplateView):
    template_name = 'contest/thanks.html'

    def get_context_data(self, **kwargs):
        return {
            'contest': kwargs.get('contest'),
        }


def get_entries_table(request, contest_id=1):
    contest = Contest.objects.get(pk=contest_id)
    entries = Entry.objects.filter(contest=contest)
    if not request.GET.__contains__('sort'):
        entries = entries.order_by('-vote_count')
    return render_to_response('contest/entry_table.html', {'contest': contest, 'entries': entries}, context_instance=RequestContext(request))


def get_winners(request, contest_id=1):
    contest = Contest.objects.get(pk=contest_id)
    entries = Entry.objects.filter(contest=contest, is_visible=True).order_by('-vote_count')
    return render_to_response('contest/winners.html', {'contest': contest, 'entries': entries}, context_instance=RequestContext(request))


def get_entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    return render_to_response('contest/entry.html', {'contest': entry.contest, 'entry': entry}, context_instance=RequestContext(request))


@login_required
def add_vote(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    contest = entry.contest
    user = User.objects.get(username=request.user)

    if contest.user_can_vote(user):
        new_vote = Vote(user=user, entry=entry)
        new_vote.save()
        entry.vote_count = entry.vote_set.count()
        entry.save()
        next_vote_date = contest.get_next_vote_date(user)
        if next_vote_date > contest.end_date:
            messages.success(request, '<div style="font-weight:bold;">Your vote has been recorded.</div>Thank you for your vote! You will not be able to vote again before the end of the contest. <br><br>Please encourage others to visit <a href="/">OpenDataCincy</a> and to join the race toward more open data!')
        else:
            messages.success(request, '<div style="font-weight:bold;">Your vote has been recorded.</div>You may vote once per week, so come back and visit us again on ' + next_vote_date.strftime('%A, %b %d %Y, %I:%M%p') + '. <br><br>Until then, encourage others to visit <a href="/">OpenDataCincy</a> and to join the race toward more open data!')
    else:
        next_vote_date = contest.get_next_vote_date(user)
        if next_vote_date > contest.end_date:
            messages.error(request, '<div style="font-weight:bold;">You have already voted.</div>You will not be able to vote again before the end of the contest. <br><br>Please encourage others to visit <a href="/">OpenDataCincy</a> and to join the race toward more open data!')
        else:
            messages.error(request, '<div style="font-weight:bold;">You have already voted.</div>You may vote once per week, so come back and visit us again on ' + next_vote_date.strftime('%A, %b %d %Y, %I:%M%p') + '. <br><br>Until then, encourage others to visit <a href="/">OpenDataCincy</a> and to join the race toward more open data!')    
    
    return redirect('/contest/?sort=vote_count')
    
