from django.shortcuts import render, get_object_or_404 , redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm, LoginForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as userlogin, logout as userlogout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.templatetags.static import static
from rest_framework import generics
from .serializers import PostSerializer





#login & signup fuctions

def homepage(request):
    return render(request,'login/home.html')


def login_page(request):
    message=''
    form = LoginForm()
    if request.method == 'POST':
    
        form = LoginForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            user = authenticate(username = formData['username'],password = formData['password'])
            
            if user is None:
                message = 'Invalid login details!'
            else:
                userlogin(request, user)
                return redirect(post_list)

    return render(request, 'login/login.html', {'form':form, 'message':message})
   

    

def register_page(request):
    message = ''
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            user = User()
            user.username = formData['username']
            user.set_password(formData['password1'])
            user.save()
            message = 'Registration done successfully'
    return render(request, 'login/register.html', {'form':form, 'message':message} )

def logout_page(request):
    userlogout(request)
    return redirect(login_page)

def delete(request):
    id = request.GET['id']
    # select * from employee where id={id}
    result = Post.objects.get(id=id)
    result.delete()
    return redirect(post_list)

@login_required(login_url='login/')
def post_list(request):
    posts = Post.objects.all()
    query = request.GET.get('q')
    if query:
        posts = posts.filter(title__icontains=query)
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts':posts})


@login_required(login_url='login/')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    pic = Post.objects.first()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
   
    return render(request, 'blog/post_detail.html', {'pic':pic,
                                                    'post':post, 
                                                    'comments': comments,
                                                    'new_comment': new_comment,
                                                    'comment_form':comment_form})
    

@login_required(login_url='login/')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')   
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
