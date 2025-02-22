from django.db.models import F
from django.http import HttpResponseRedirect
from polls.models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "last_five_questions"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_id = request.POST["choice"]

    try:
        choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        choice.votes = F("votes") + 1
        choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
