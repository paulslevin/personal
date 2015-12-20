from django.shortcuts import render
from django.http import HttpResponse
from .models import Composition


def index(request):
    pieces = Composition.objects.all()
    context = {"pieces": pieces}
    return render(request, 'music/index.html', context)
