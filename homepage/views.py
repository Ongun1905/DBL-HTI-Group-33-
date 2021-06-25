from django.conf import settings  # Import settings to allow BASE_DIR to be used
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.mail import message, send_mail, BadHeaderError
from .visualizations import adjacency_matrix
from .forms import UploadFileForm
from .forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect
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
    #added for contact form
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            Your_Email = form.cleaned_data["Your_Email"]
            message = form.cleaned_data["message"]
            try:
                send_mail(Your_Email, message, subject, ["dblgroup3333@gmail.com"])
            except BadHeaderError:
                return ("Invalid header found.")
            return redirect("success")
    return render(request, "homepage/about.html", {"form": form})


def vis1(request): 
    return render(request, "homepage/vis1.html")

def vis2(request):
    # Fetch data from the adjacency matrix vis file
    matrix, nodeInfo, edges = adjacency_matrix.getMultiMatrix()
    normalizedMatrix = adjacency_matrix.getNormalizedMultiMatrix(1)
    sentimentMatrix = adjacency_matrix.getSentimentMultiMatrix(1)
    hasEdges = True

    if (len(edges) < 1):
        hasEdges = False

    # Create the data object to pass to the view
    matrixDataObject = {
        # Combine the data ("zipping" the data) to allow iterating over multiple lists asynchronously
        "zippedMatrixData": zip(matrix, normalizedMatrix, sentimentMatrix, nodeInfo),
        "edgeData": json.dumps(edges),
        "nodeData": nodeInfo,
        "hasEdges": hasEdges
    }
        
    return render(request, "homepage/vis2.html", matrixDataObject)

def vis3(request): 
    # Fetch data from the adjacency matrix vis file
    matrix, nodeInfo, edges = adjacency_matrix.getMultiMatrix()
    normalizedMatrix = adjacency_matrix.getNormalizedMultiMatrix(1)

    hasEdges = True
    if (len(edges) < 1):
        hasEdges = False

    # Create the data object to pass to the view
    matrixDataObject = {
        # Combine the data ("zipping" the data) to allow iterating over multiple lists asynchronously
        "zippedMatrixData": zip(matrix, normalizedMatrix, nodeInfo),
        "edgeData": json.dumps(edges),
        "nodeData": nodeInfo,
        "hasEdges": hasEdges
    }
    return render(request, "homepage/vis3.html", matrixDataObject)

def successView(request):
    return HttpResponse('Success! Thank you for your message')
