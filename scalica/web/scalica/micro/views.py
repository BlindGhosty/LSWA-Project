from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Following, Post, FollowingForm, PostForm, MyUserCreationForm, Recommendation

import grpc
import backend_pb2
import backend_pb2_grpc

# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'micro/public.html')

def stream(request, user_id):
  # See if to present a 'follow' button
  form = None
  if request.user.is_authenticated() and request.user.id != int(user_id):
    try:
      f = Following.objects.get(follower_id=request.user.id,
                                followee_id=user_id)
    except Following.DoesNotExist:
      form = FollowingForm
  user = User.objects.get(pk=user_id)
  post_list = Post.objects.filter(user_id=user_id).order_by('-pub_date')
  paginator = Paginator(post_list, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    posts = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    posts = paginator.page(paginator.num_pages)
  context = {
    'posts' : posts,
    'stream_user' : user,
    'form' : form,
  }
  return render(request, 'micro/stream.html', context)

def register(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    new_user = form.save(commit=True)
    # Log in that user.
    user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if user is not None:
        login(request, user)
        """
        so I think the mapping starts here at login
        grab all the ids I follow, grab all the ids they follow
            (+ grab stuff they follow???)
            This would be easier if the rpc just had access to the same db as scalica
        Then send the whole unsanitized list out?

        On the rpc side, Take the list of ids. To scale, break up this list, but for now let's skip that.
        Reduce the instances by counting the userIds up, send back to the scalica server

        When scalica receives back a list of ids from the rpc,
            save that to the recommendation db (should be cached tbh)
            serve this on recommendation requests
            ? If scalica doesn't have any suggestions, just shoot back random users?

        ! Actually, what if the rpc just saved straight after it finished rather then send it back?
        When a user logs in to Scalica, the appserver will send an RPC to your simple RPC server,
        who will read the recommendations for the user and send them back to Scalica, where you will present them.
        """
    else:
      raise Exception
    return home(request)
  else:
    form = MyUserCreationForm
  return render(request, 'micro/register.html', {'form' : form})

# Authenticated views
#####################
@login_required
def home(request):
  '''List of recent posts by people I follow'''
  try:
    my_post = Post.objects.filter(user=request.user).order_by('-pub_date')[0]
  except IndexError:
    my_post = None
  follows = [o.followee_id for o in Following.objects.filter(
    follower_id=request.user.id)]
  post_list = Post.objects.filter(
      user_id__in=follows).order_by('-pub_date')[0:10]
  context = {
    'post_list': post_list,
    'my_post' : my_post,
    'post_form' : PostForm
  }
  return render(request, 'micro/home.html', context)

# Allows to post something and shows my most recent posts.
@login_required
def post(request):
  if request.method == 'POST':
    form = PostForm(request.POST)
    new_post = form.save(commit=False)
    new_post.user = request.user
    new_post.pub_date = timezone.now()
    new_post.save()
    return home(request)
  else:
    form = PostForm
  return render(request, 'micro/post.html', {'form' : form})

@login_required
def follow(request):
  if request.method == 'POST':
    form = FollowingForm(request.POST)
    new_follow = form.save(commit=False)
    new_follow.follower = request.user
    new_follow.follow_date = timezone.now()
    new_follow.save()
    return home(request)
  else:
    form = FollowingForm
  return render(request, 'micro/follow.html', {'form' : form})

# Our Recommendation Service:
#############################
@login_required
def recommend(request):
    follow_results = Following.objects.filter(follower_id=request.user).order_by('-follow_date')
    try:
        rec_results = Recommendation.objects.filter(user=request.user)
    except:
        print 'problem?'

    context = {
        'follows': follow_results,
        'recs': rec_results,
    }
    return render(request, 'micro/recommend.html', context)

@login_required
def testRPC(request):
    channel = grpc.insecure_channel('localhost:20426')
    stub = backend_pb2_grpc.GenerateFollowersStub(channel)
    userId = request.user.id
    followIds = Following.objects.filter(follower_id=request.user).values_list('followee_id', flat=True)
    for i in followIds:
      follower2_id = User.objects.get(id=i)
      followIds2 = Following.objects.filter(follower_id=follower2_id).values_list('followee_id', flat=True)
      request = backend_pb2.FollowerRequest(MainUserId=userId, SubscriptionsId=followIds, PossFollowersId=followIds2)
      request = backend_pb2.FollowerRequest(MainUserId=userId, SubscriptionsId=request_arr)
      response = stub.logic1(request)
      if response:
        print "The recommendation is that you for user " +  User.objects.get(pk=i).username;
      
