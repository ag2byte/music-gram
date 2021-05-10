from collections import OrderedDict

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
import pprint
# from .spotify_api import SpotifyAPI,milli

from .spotify_api import SpotifyAPI, milli

import shortuuid as suid
import sys
import pyrebase

client_id = '46d058fd7fd24823a92ec77bcd794c23'
client_secret = '3e43a088cfb9476fa0a1436e9dc8614b'

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
final_result = {}
final_result_dict = {}
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
    # currentUser = firebaseauth.current_user

    # displayName = firebasedb.child('users').order_by_child('email').equal_to(currentUser['email']).get()
    # print(displayName.val())
    # if(currentUser):
    return render(request, 'feed.html')
    # else:
    #     return HttpResponse('You need to sign in to see this page')

def addpost(request):
    # currentUser = firebaseauth.current_user
        # pprint(final_result)
    # if currentUser:
    return render(request, 'addpost.html')
    # else:
    #     return HttpResponse('You need to sign in to see this page')

def bookmarks(request):
    # currentUser = firebaseauth.current_user
    # if currentUser:
    return render(request, 'bookmarks.html')
    # else:
    #     return HttpResponse('You need to sign in to see this page')


def follow():
    # this function is incomplete still as it will be connected to the frontend and the names' Abhi' and ' Gojou' will come from the frontend
    # however this is the basic function of following 

    follower = firebasedb.child('users').order_by_child('displayName').equal_to('Abhi').limit_to_first(1).get().val()
    follower_id = list(follower)[0]  # this is the id finally
    follower_name = list(follower.values())[0].get('displayName')
    followed = firebasedb.child('users').order_by_child('displayName').equal_to('Gojou').limit_to_first(1).get().val()
    followed_id = list(followed)[0]
    followed_name = list(followed.values())[0].get('displayName')
    print('followerdet:', follower)
    print('followername:',follower_name )
    print('followerid', follower_id)
    print('followed:',followed)
    print('followedid :', followed_id)
    print('followedname:',followed_name )
    
    # adding Abhi as the follower of Gojou

    firebasedb.child('users').child(followed_id).child('followers').set({follower_id:follower_name})# adding follower for followed
    firebasedb.child('users').child(follower_id).child('following').set({followed_id:followed_name})# adding follwed for follower
    
    # end of db following feature

    
def search_song(request):
    spotify1 = SpotifyAPI(client_id, client_secret)
    spotify1.perform_auth()
    name =  request.POST['song_name']
    print(f'song name: {name} \n')
    result = spotify1.search({"track":name},search_type="track")
    # print(f'result : {result} \n ')
    total_no_result = len(result["tracks"]["items"])
    final_result_list = []
    final_result = {}
    for i in range(0,total_no_result//2):
        final_result["name"] =  result["tracks"]["items"][i]['name']
        final_result["artist"] = result["tracks"]["items"][i]['artists'][0]['name']
        # final_result["available_india"] = 'IN' in result["tracks"]["items"][i]['album']['available_markets']
        # final_result["images"] = result["tracks"]["items"][i]['album']['images'][0]['url']
        # final_result["link"] =  result["tracks"]["items"][i]['external_urls']['spotify']
        # final_result["explicit"] = result["tracks"]["items"][i]["explicit"]
        # final_result["duration"] = milli(result["tracks"]["items"][i]["duration_ms"])
        print(f"final_result: {final_result} \n")
        final_result_list.append(final_result)
        # print(final_result_dict)
        print('\n')

    return render(request, "addpost.html",{'link': final_result_list})
    

def testfunction(request):
    
  
    
    
  
    return  HttpResponse('hellotester')