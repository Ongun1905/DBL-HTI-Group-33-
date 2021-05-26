from django.shortcuts import render
from django.http import HttpResponse
from .visualizations import adjacency_matrix
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
def index(request): 
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        if uploaded_file.name in os.listdir('media'):
            name = os.listdir('media')[-1][:-4] + '1.csv'
        else:
            name = uploaded_file.name
        filename = fs.save(name, uploaded_file)
        uploaded_file_url = fs.url(filename)
        return render(request, "homepage/index.html", {"uploaded_file_url":"uploaded file: " + filename} )
    return render(request, "homepage/index.html")

def about(request):
    return render(request, "homepage/about.html")

def vis1(request): 
    return render(request, "homepage/vis1.html")

def vis2(request):
    normalizedMatrix, nodeInfo = adjacency_matrix.getNormalizedMultiMatrix(255)
    zippedMatrix = zip(normalizedMatrix, nodeInfo)
        
    return render(request, "homepage/vis2.html", {"adj_matrix": zip(normalizedMatrix, nodeInfo), "adj_matrix_2": zip(normalizedMatrix, nodeInfo)})