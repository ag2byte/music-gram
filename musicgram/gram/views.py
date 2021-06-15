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

client_id = 'YOUR_CLIENT_ID_SPOTIFY'
client_secret = 'YOUR_CLIENT_SECRET_key'


firebaseconfig = {
    'apiKey': "APIKEY",
    'authDomain': "AUTHDOMAIN",
    'projectId': "PROJECTID",
    'databaseURL': "DATABASEURL",

    'storageBucket': "STORAGEBUCKET",
    'messagingSenderId': "MESSAGINGSENDERID",
    'appId': "APPID",
    'measurementId': "MEASUREMENTID"

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
                    
                    request.session['userid'] = i.key()
                    
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
        data = {'displayName':displayName, 'email':email} # 'followers':0, 'following':0,
        
        print(id, data)
        firebasedb.child('users').child(id).set(data)
        # we need to add email verification as well
        # add success toast after this and redirect to login page
        # return render(request,'index.html',{'errormessage':'Signup Successful! Lets log you in'}) 
        return HttpResponseRedirect(reverse('index'))
        
    return render(request,'signup.html')

def feed(request):
   
    try:
        # request.session['userid']):
        likedposts = firebasedb.child('posts').order_by_child('likes').start_at(1).get()
        likedlist = []
        for i in likedposts.each():
            skey  = i.key()
            
            fposts = firebasedb.child('posts').child(skey).child('liked_by').get()
            for j in fposts:
                if j.val() == request.session['userid']:
                    
                    likedlist.append(i.key())

    
        posts = firebasedb.child("posts").get()
        postlist = []
        for item in posts.each():
            postlist.append({item.key():item.val()})
        print(postlist.reverse())
        bookmarklist = []
        for i in posts.each():
            if 'bookmarked_by' in i.val():
                if request.session['userid'] in i.val()['bookmarked_by'].values():
                    bookmarklist.append(i.key())
     
        return render(request, 'feed.html',{ 'username' : request.session['displayName'],'postlist':postlist,'likedlist':likedlist,'bookmarklist':bookmarklist})
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
            
            return JsonResponse({},status = 201)


        
        return render(request, 'addpost.html')
    except:
        return HttpResponse('You need to sign in to see this page')

def bookmarks(request):
    try:
        # request.session['userid']):
        likedposts = firebasedb.child('posts').order_by_child('likes').start_at(1).get()
        likedlist = []
        for i in likedposts.each():
            skey  = i.key()
            
            fposts = firebasedb.child('posts').child(skey).child('liked_by').get()
            for j in fposts:
                if j.val() == request.session['userid']:
                   
                    likedlist.append(i.key())

     
      
        posts = firebasedb.child("posts").get()
        postlist = []
        for item in posts.each():
            postlist.append({item.key():item.val()})
        print(postlist.reverse())
        bookmarklist = []
        for i in posts.each():
            if 'bookmarked_by' in i.val():
                if request.session['userid'] in i.val()['bookmarked_by'].values():
                    bookmarklist.append(i.key())
            

        return render(request, 'bookmarks.html',{ 'username' : request.session['displayName'],'postlist':postlist,'likedlist':likedlist,'bookmarklist':bookmarklist})
    except Exception as e: 
        print(e)
        return HttpResponse('You need to sign in to see this page')


# @csrf_exempt
def createpost(request):
    try:
        currentuser = request.session['userid']
        song = request.session['newpostsong']
  
        print("song from createpost", song)
        if request.method == 'POST':
            caption = request.POST['caption']
     
            data = {'displayName':request.session['displayName'], 
                                            'caption':caption, 
                                            'songname':song['songname'],
                                            'artist':song['artist'],
                                            'imagelink':song['imagelink'],
                                            'songlink':song['songlink'],
                                            'likes':0,
                                            
                                             } 
         
            firebasedb.child('posts').push(data)
            return HttpResponseRedirect(reverse('feed'))

        return render(request,'createpost.html',{'song':song})
    except:
        return HttpResponse("Unauthorised to access the url")
@csrf_exempt
def follow(request):
 

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
    
  

    firebasedb.child('users').child(followed_id).child('followers').push(follower_id)# adding follower for followed
    firebasedb.child('users').child(follower_id).child('following').push(followed_id)# adding follwed for follower
    return JsonResponse({},status = 201)




@csrf_exempt
def unfollow(request):
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
    


    firebasedb.child('users').child(followed_id).child('followers').child(follower_id).remove()# adding follower for followed
    firebasedb.child('users').child(follower_id).child('following').child(followed_id).remove()# adding follwed for follower
    return JsonResponse({},status = 201)

def search_song(request):
    
    name =  request.POST['song_name']
   
    final_result_list = searchSong(name)
 
    return render(request, "addpost.html",{'link': final_result_list})

@csrf_exempt
def like(request):
    try:
        songid = json.loads(request.body.decode('utf-8'))['songid']
        
   
        song = firebasedb.child('posts').child(songid).get().val()
        firebasedb.child('posts').child(songid).child('liked_by').push(request.session['userid'])
        
        print(songid,request.session['userid'])
        likes = song['likes']
        firebasedb.child('posts').child(songid).update({'likes':likes+1})

        return JsonResponse({},status = 201)
    except Exception as e:
        print(e)
        return HttpResponse('Something went wrong')


@csrf_exempt
def unlike(request):
    try:
        songid = json.loads(request.body.decode('utf-8'))['songid']
        song = firebasedb.child('posts').child(songid).get().val()
        posts = firebasedb.child('posts').child(songid).child('liked_by').get()
        rkey = ''
        for i in posts:
            if i.val() == request.session['userid']:
                rkey = i.key()
        # now delete the like

    
       

        firebasedb.child('posts').child(songid).child('liked_by').child(rkey).remove()
        
       
        likes = song['likes']
        firebasedb.child('posts').child(songid).update({'likes':likes-1})

        return JsonResponse({},status = 201)
    except Exception as e:
        print(e)
        return HttpResponse('Something went wrong')



     
def profile(request,displayname):
    # get profile for a displayname 
    try:
        user = firebasedb.child("users").order_by_child("displayName").equal_to(displayname).get()
        
        followers, following = 0,0

        toFollow = 1

        if request.session['displayName'] == displayname:
            toFollow = 0
        for i in user.each():
            
            if 'followers' in i.val():
                followers = len(i.val()['followers'])
                # check if there is a need to follow:

                if request.session['userid'] in i.val()['followers'].values():
                    # either is it own profile or already followed
                    print("same name")
                    toFollow = -1
            if 'following' in i.val():
                following = len(i.val()['following'])
        likedposts = firebasedb.child('posts').order_by_child('likes').start_at(1).get()
        likedlist = []
        for i in likedposts.each():
            skey  = i.key()
          
            fposts = firebasedb.child('posts').child(skey).child('liked_by').get()
            for j in fposts:
                if j.val() == request.session['userid']:
                    
                    likedlist.append(i.key())

     
        posts = firebasedb.child("posts").order_by_child("displayName").equal_to(displayname).get()
        postlist = []
        for item in posts.each():
                postlist.append({item.key():item.val()})


        print(postlist.reverse())

        bookmarklist = []
        for i in posts.each():
            if 'bookmarked_by' in i.val():
                if request.session['userid'] in i.val()['bookmarked_by'].values():
                    bookmarklist.append(i.key())
            

       
        

        return render(request, "profile.html",{'displayName': displayname, 'followers':followers, 'following':following, 'toFollow':toFollow ,'postlist':postlist,'likedlist':likedlist,'bookmarklist':bookmarklist})
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")



@csrf_exempt
def bookmark(request):
    try:
        songid = json.loads(request.body.decode('utf-8'))['songid']
   
        song = firebasedb.child('posts').child(songid).get().val()
        firebasedb.child('posts').child(songid).child('bookmarked_by').push(request.session['userid'])
        

        return JsonResponse({},status = 201)
    except Exception as e:
        print(e)
        return HttpResponse('Something went wrong')


@csrf_exempt
def unbookmark(request):
    try:
        songid = json.loads(request.body.decode('utf-8'))['songid']
        song = firebasedb.child('posts').child(songid).get().val()
        posts = firebasedb.child('posts').child(songid).child('bookmarked_by').get()
        rkey = ''
        for i in posts:
            if i.val() == request.session['userid']:
                rkey = i.key()
                break
        # now delete the like

    
      

        firebasedb.child('posts').child(songid).child('bookmarked_by').child(rkey).remove()
        
        

        return JsonResponse({},status = 201)
    except Exception as e:
        print(e)
        return HttpResponse('Something went wrong')
