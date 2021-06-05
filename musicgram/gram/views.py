from collections import OrderedDict

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth,sessions
import pprint

from requests.adapters import HTTPResponse
from requests.api import post
# from .spotify_api import SpotifyAPI,milli

from .spotify_api import SpotifyAPI, milli, searchSong

import shortuuid as suid
import sys
import pyrebase
import datetime
import json

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
        # print(email, password)
        try:
            user = firebaseauth.sign_in_with_email_and_password(email, password) #firebase authentication
            if user:
                print(user['email'])
                # print('sessionid:', user['idToken'])
                test = firebasedb.child("users").order_by_child('email').equal_to(user['email']).get()
                request.session['useremail'] = user['email']
                for i in test.each():
                    print(i.key())
                    request.session['userid'] = i.key()
                    print(i.val())
                    print(i.val()['displayName'])
                    request.session['displayName'] = i.val()['displayName']
                    
                session_id = user['idToken']
                request.session['uid'] = str(session_id)  # creating a session


                # get displayName and id from the realtime  database and add to session for easier access
                return HttpResponseRedirect(reverse('feed'))

        except:
            errormessage = 'Invalid Credentials'
            return render(request,'index.html',{'errormessage':errormessage}) 
        

    return render(request, 'index.html')

def logout(request):

    # currentUser = firebaseauth.current_user
    
    try:
        del request.session['uid'] 
        del request.session['userid'] 
        del request.session['displayName'] 
        del request.session['useremail']
                # firebaseauth.signOut()
                # auth.logout(request)
    except KeyError:
        return HttpResponse('You cannot access this url now')
    return HttpResponseRedirect(reverse('index'))
    
        

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
   
    try:
        # request.session['userid']):
        posts = firebasedb.child("posts").get()
        postlist = []
        for item in posts.each():
            postlist.append({item.key():item.val()})
        print(postlist)
        # print(postlist)
        # for dic in postlist:
        #     for i in dic:
        #         print(i,dic[i])
        return render(request, 'feed.html',{ 'username' : request.session['displayName'],'postlist':postlist})
    except Exception as e: 
        print(e)
        return HttpResponse('You need to sign in to see this page')
@csrf_exempt
def addpost(request):
    try:
        currentuser = request.session['userid']
        if request.method == 'POST':
            song = json.loads(request.body.decode('utf-8'))['value']
            print(" song in add post", song)
            request.session['newpostsong'] = song
            t = request.session['newpostsong']
            print("t",t)
            #  createpost(request)
            return JsonResponse({},status = 201)


        # if currentUser:
        return render(request, 'addpost.html')
    except:
        return HttpResponse('You need to sign in to see this page')

def bookmarks(request):
    # currentUser = firebaseauth.current_user
    # if currentUser:
    return render(request, 'bookmarks.html')
    # else:
    #     return HttpResponse('You need to sign in to see this page')


# @csrf_exempt
def createpost(request):
    try:
        currentuser = request.session['userid']
        song = request.session['newpostsong']
        # print(request.session['newpostsong'])
        print("song from createpost", song)
        if request.method == 'POST':
            caption = request.POST['caption']
            id = suid.uuid()
            data = {'displayName':request.session['displayName'], 
                                            'caption':caption, 
                                            'songname':song['songname'],
                                            'artist':song['artist'],
                                            'imagelink':song['imagelink'],
                                            'songlink':song['songlink'],
                                            'likes':0,
                                            # 'datetime':datetime.datetime.now()
                                             } 
            print(id, data)
            firebasedb.child('posts').child(id).set(data)
            return HttpResponseRedirect(reverse('feed'))

        return render(request,'createpost.html',{'song':song})
    except:
        return HttpResponse("Unauthorised to access the url")
@csrf_exempt
def follow(request):
    # this function is incomplete still as it will be connected to the frontend and the names' Abhi' and ' Gojou' will come from the frontend
    # however this is the basic function of following 

    to_be_followed = json.loads(request.body.decode('utf-8'))['to_be_followed']
    followed_by = json.loads(request.body.decode('utf-8'))['followed_by']
    print(to_be_followed,followed_by)

    follower = firebasedb.child('users').order_by_child('displayName').equal_to(followed_by).limit_to_first(1).get().val()
    follower_id = list(follower)[0]  # this is the id finally
    follower_name = list(follower.values())[0].get('displayName')
    followed = firebasedb.child('users').order_by_child('displayName').equal_to(to_be_followed).limit_to_first(1).get().val()
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
    return JsonResponse({},status = 201)

    # end of db following feature

    
def search_song(request):
    
    name =  request.POST['song_name']
    print(f'song name: {name} \n')
    final_result_list = searchSong(name)
    print(final_result_list[0]['name'])
    return render(request, "addpost.html",{'link': final_result_list})
    
@csrf_exempt
def testfunction(request):
    to_be_followed = json.loads(request.body.decode('utf-8'))['to_be_followed']
    followed_by = json.loads(request.body.decode('utf-8'))['followed_by']
    print(to_be_followed,followed_by)
    return JsonResponse({},status = 201)

     
def profile(request,displayname):
    # get profile for a displayname 
    try:
        user = firebasedb.child("users").order_by_child("displayName").equal_to(displayname).get()
        
        followers, following = 0,0

        toFollow = True

        if request.session['displayName'] == displayname:
            toFollow = False
        for i in user.each():
            
            if 'followers' in i.val():
                followers = len(i.val()['followers'])
                # check if there is a need to follow:

                if request.session['userid'] in i.val()['followers'].keys():
                    # either is it own profile or already followed
                    print("same name")
                    toFollow = False
            if 'following' in i.val():
                following = len(i.val()['following'])

        posts = firebasedb.child("posts").order_by_child("displayName").equal_to(displayname).get()
        postlist = []
        for item in posts.each():
                postlist.append({item.key():item.val()})


        print(i.key())

        return render(request, "profile.html",{'displayName': displayname, 'followers':followers, 'following':following, 'toFollow':toFollow ,'postlist':postlist})
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")