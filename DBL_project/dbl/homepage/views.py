# Import settings to allow BASE_DIR to be used
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse
from .visualizations import adjacency_matrix
from django.core.files.storage import FileSystemStorage
import os
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
# Create your views here.
def index(request): 
    if request.method == 'POST':
        # Take it data the user sbmitted and save it as a form 
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            if uploaded_file.name in os.listdir(settings.BASE_DIR / 'media'):
                name = os.listdir(settings.BASE_DIR / 'media')[-1][:-4] + '1.csv'
            else:
                name = uploaded_file.name
            filename = fs.save(name, uploaded_file)
            uploaded_file_url = fs.url(filename)
            return render(request, "homepage/index.html", {
                "uploaded_file_url":"uploaded file: " + filename,
                "form":form})
    
    return render(request, "homepage/index.html", {
        "uploaded_file_url":"You have not uploaded any file", 
        "form":UploadFileForm()})

def about(request):
    return render(request, "homepage/about.html")

def vis1(request): 
    return render(request, "homepage/vis1.html")

def vis2(request):
    normalizedMatrix, nodeInfo = adjacency_matrix.getNormalizedMultiMatrix(255)
    zippedMatrix = zip(normalizedMatrix, nodeInfo)
        
    return render(request, "homepage/vis2.html", {"adj_matrix": zip(normalizedMatrix, nodeInfo), "adj_matrix_2": zip(normalizedMatrix, nodeInfo)})

def vis_combined(request): 
    return render(request, "homepage/vis_combined.html")