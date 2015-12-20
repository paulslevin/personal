from django.shortcuts import render
from django.http import HttpResponse

from .models import Paper, Coauthor

def research(request):
    latest_papers = Paper.objects.order_by('publish_date')
    context = {'latest_papers': latest_papers,
    }
    return render(request, 'research/index.html', context)
