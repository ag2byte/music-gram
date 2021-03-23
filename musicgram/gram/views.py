from collections import OrderedDict

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth

import shortuuid as suid
import pyrebase

"firebase part : DO NOT MESS WITH THIS"
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
firebaseauth = firebase.auth()
firebasedb = firebase.database()
# firebase part end

# Create your views here.
def index(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password'] # signin info
        print(email, password)
        try:
            user = firebaseauth.sign_in_with_email_and_password(email, password) #firebase authentication
            if user:
                print(user['email'])
                # print('sessionid:', user['idToken'])
                session_id = user['idToken']
                request.session['uid'] = str(session_id)  # creating a session
                return HttpResponseRedirect(reverse('feed'))

        except:
            errormessage = 'Invalid Credentials'
            return render(request,'index.html',{'errormessage':errormessage}) 
        

    return render(request, 'index.html')

def logout(request):

    currentUser = firebaseauth.current_user
    if(currentUser):
        try:
            del request.session['uid']
            # firebaseauth.signOut()
            # auth.logout(request)
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('You cannot access this url now')

def signup(request):
    if request.method == 'POST':
        displayName = request.POST['displayName']
        email = request.POST['email']
        password = request.POST['password']
        print({displayName}, {email}, {password})
        firebaseauth.create_user_with_email_and_password(email, password)
        
        # adding into database
        id = suid.uuid()
        data = {'displayName':displayName, 'email':email, 'posts': 0 } # 'followers':0, 'following':0,
        
        print(id, data)
        firebasedb.child('users').child(id).set(data)
        # we need to add email verification as well
        # add success toast after this and redirect to login page

        
    return render(request,'signup.html')

def feed(request):
    currentUser = firebaseauth.current_user

    # displayName = firebasedb.child('users').order_by_child('email').equal_to(currentUser['email']).get()
    # print(displayName.val())
    if(currentUser):
        return render(request, 'feed.html')
    else:
        return HttpResponse('You need to sign in to see this page')

def addpost(request):
    currentUser = firebaseauth.current_user
    if currentUser:
        return render(request, 'addpost.html')
    else:
        return HttpResponse('You need to sign in to see this page')
def bookmarks(request):
    currentUser = firebaseauth.current_user
    if currentUser:
        return render(request, 'bookmarks.html')
    else:
        return HttpResponse('You need to sign in to see this page')


def testfunction(request):
    
  
    # working demo of following feature in db
    # user1 = firebasedb.child('users').order_by_child('displayName').equal_to('Abhi').limit_to_first(1).get().val()
    # user1_id = list(user1)[0]  # this is the id finally
    # user1_name = list(user1.values())[0].get('displayName')
    # user2 = firebasedb.child('users').order_by_child('displayName').equal_to('Gojou').limit_to_first(1).get().val()
    # user2_id = list(user2)[0]
    # user2_name = list(user2.values())[0].get('displayName')
    # print('user1det:', user1)
    # print('user1name:',user1_name )
    # print('user1id', user1_id)
    # print('user2det:',user2)
    # print('user2id :', user2_id)
    # print('user2name:',user2_name )
    
    # adding Abhi as the follower of Gojou
    # firebasedb.child('followedby').child(user2_id).set({user1_id: user1_name})
    # firebasedb.child('follows').child(user1_id).set({user2_id: user2_name})

    # {REMAINING}: update values in followers and followers field in users children
    # end of db following feature
    
    
  
    return  HttpResponse('hellotester')