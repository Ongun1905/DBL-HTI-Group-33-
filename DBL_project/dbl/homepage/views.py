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
    # Fetch data from the adjacency matrix vis file
    matrix, nodeInfo = adjacency_matrix.getMultiMatrix()
    normalizedMatrix = adjacency_matrix.getNormalizedMultiMatrix(1)

    # Create the data object to pass to the view
    matrixDataObject = {
        # Combine the data ("zipping" the data) to allow iterating over multiple lists asynchronously
        "zippedMatrixData": zip(matrix, normalizedMatrix, nodeInfo),
        "nodeData": nodeInfo
    }
        
    return render(request, "homepage/vis2.html", matrixDataObject)
