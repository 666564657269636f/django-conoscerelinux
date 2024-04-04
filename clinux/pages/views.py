from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import StaticPage


def index(request):
    return render(request, "pages/index.html", {
        "pages_list": StaticPage.objects.all()
    })

def detail(request, slug):
    page = get_object_or_404(StaticPage, slug=slug)
    return render(request, "pages/detail.html", {
        "page": page
    })
    
