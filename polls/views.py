from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse("Hello, world. You're at the polls index.")
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list' : latest_question_list,
    }
    # return HttpResponse(output)
    # return HttpResponse(template.render(context,request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # response = "You are looking at the question number %s"
    # return HttpResponse(response % question_id)

    #Method 1
    # try:
    #     question = Question.objects.get(pk = question_id)
    #     context = {
    #         'question' : question,
    #     }
    # except Question.DoesNotExist:
    #     raise Http404("Page Does not exists")
    # return render(request, 'polls/detail.html',context)

    #shortcut method
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question' : question})


def results(request, question_id):
    # response = "You're looking at the results of question %s."
    question = get_object_or_404(Question, pk = question_id)
    # return HttpResponse(response % question_id)
    return render(request, 'polls/results.html', {'question' : question})
def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk= request.POST['choice'])
    except:
        return render(request , 'polls/detail.html',{
            'question' : question,
            'error_message' : 'You did not select a choice',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("You are voting on the question %s" % question_id)