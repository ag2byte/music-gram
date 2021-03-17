from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


import pyrebase


firebaseconfig = {
    'apiKey': "AIzaSyBHki4FC5c9dMPTf4gA_axvHQaezJoJN90",
    'authDomain': "musicgram-69420.firebaseapp.com",
    'projectId': "musicgram-69420",
    'databaseURL': "https://musicgram-69420-default-rtdb.firebaseio.com",

    'storageBucket': "musicgram-69420.appspot.com",
    'messagingSenderId': "319646960925",
    'appId': "1:319646960925:web:c67c9d32c9b02efb1725f4",
    'measurementId': "G-WZHBNPQYRC"

}

firebase = pyrebase.initialize_app(firebaseconfig)
auth = firebase.auth()


# Create your views here.
def index(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            if user:
                print(user['email'])
        except:
            print('Invalid credentials')
        

    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        displayName = request.POST['displayName']
        email = request.POST['email']
        password = request.POST['password']
        print({displayName}, {email}, {password})
        user = auth.create_user_with_email_and_password(email, password)
        # user.update({
        #     'displayName':displayName
        # })
    return render(request,'signup.html')

def feed(request):
    return render(request, 'feed.html')

def addpost(request):
    return render(request, 'addpost.html')
def bookmarks(request):
    return render(request,'bookmarks.html')