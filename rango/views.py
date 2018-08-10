from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'boldmessage': 'Ooops, a template!'
    }

    return render(request, 'rango/index.html', context=context)


def about(request):
    context = {
        'myname': 'Jesus'
    }

    return render(request, 'rango/about.html', context=context)
