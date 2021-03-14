from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')
def feed(request):
    return render(request, 'feed.html')

def addpost(request):
    return render(request, 'addpost.html')
def bookmarks(request):
    return render(request,'bookmarks.html')