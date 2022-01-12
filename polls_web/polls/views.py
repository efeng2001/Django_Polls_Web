from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


#def index(request):
#    latest_question_list = Question.objects.order_by("-pub_date")[:5]
#    context = {
#        "latest_question_list": latest_question_list
#    }
#    return render(request, "polls/index.html", context)

#def detail(request, question_id):
#    #try:
#    #   question = Question.objects.get(id = question_id)
#    #except Question.DoesNotExist:
#    #    raise Http404("Question does not exist")

#    #pk for primary key 
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})

#def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        #get the selected choice
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
        #add a vote to that choice
        selected_choice.votes += 1
        #save
        selected_choice.save()
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
        {
            'question': question, 
            'error_message': "You didn't select a choice"
        })
    #redirect to the results page
    return redirect("polls:results", pk = question.id)