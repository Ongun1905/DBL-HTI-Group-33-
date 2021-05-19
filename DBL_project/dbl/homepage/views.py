from django.shortcuts import render
from django.http import HttpResponse
from .visualizations import adjacency_matrix
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request): 
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save("enron-v1.csv", uploaded_file)
    return render(request, "homepage/index.html")

def about(request):
    return render(request, "homepage/about.html")

def vis1(request): 
    return render(request, "homepage/vis1.html")

def vis2(request):
    matrix = adjacency_matrix.getNormalizedMultiMatrix(255)
    return render(request, "homepage/vis2.html", {"matrix": matrix})

