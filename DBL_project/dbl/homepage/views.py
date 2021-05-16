from django.shortcuts import render
from django.http import HttpResponse
from .visualizations import adjacency_matrix

# Create your views here.
def index(request): 
    return render(request, "homepage/index.html")

def about(request):
    return render(request, "homepage/about.html")

def vis1(request): 
    return render(request, "homepage/vis1.html")

def vis2(request):
    matrix = adjacency_matrix.getNormalizedMultiMatrix(255)
    return render(request, "homepage/vis2.html", {"matrix": matrix})