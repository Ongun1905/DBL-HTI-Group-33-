from django.conf import settings  # Import settings to allow BASE_DIR to be used
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .visualizations import adjacency_matrix
from .forms import UploadFileForm
import os
import json

# Create your views here.
def index(request):
    if request.method == 'POST':
        # Take it data the user submitted and save it as a form
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
                "has_uploaded_file": True,
                "uploaded_file_url": filename,
                "form": form
            })
    
    return render(request, "homepage/index.html", {
        "has_uploaded_file": False,
        "uploaded_file_url": "No file selected",
        "form": UploadFileForm(auto_id=False)
    })

def about(request):
    return render(request, "homepage/about.html")

def vis1(request): 
    return render(request, "homepage/vis1.html")

def vis2(request):
    # Fetch data from the adjacency matrix vis file
    matrix, nodeInfo, edges = adjacency_matrix.getMultiMatrix()
    normalizedMatrix = adjacency_matrix.getNormalizedMultiMatrix(1)

    # Create the data object to pass to the view
    matrixDataObject = {
        # Combine the data ("zipping" the data) to allow iterating over multiple lists asynchronously
        "zippedMatrixData": zip(matrix, normalizedMatrix, nodeInfo),
        "edgeData": json.dumps(edges),
        "nodeData": nodeInfo
    }
        
    return render(request, "homepage/vis2.html", matrixDataObject)

def vis3(request):
    # Fetch data from the adjacency matrix vis file
    matrix, nodeInfo, edges = adjacency_matrix.getMultiMatrix()
    normalizedMatrix = adjacency_matrix.getNormalizedMultiMatrix(1)

    # Create the data object to pass to the view
    matrixDataObject = {
        # Combine the data ("zipping" the data) to allow iterating over multiple lists asynchronously
        "zippedMatrixData": zip(matrix, normalizedMatrix, nodeInfo),
        "edgeData": json.dumps(edges),
        "nodeData": nodeInfo
    }
    return render(request, "homepage/vis3.html", matrixDataObject)
