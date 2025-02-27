from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import CreatePostForm
from .models import Post

# Create your views here.

def blog_view(request:HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    return render(request, 'main/home.html', {"posts" : posts})


def post_view(request:HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if Post.objects.filter(title=title).exists():
                form.add_error('title', 'A post with this title already exists.')
                return render(request, 'main/post.html', {'form' : form})
            else:
                new_post = Post(title = request.POST["title"], 
                                content = request.POST["content"], 
                                category = request.POST["category"], 
                                publish_date = request.POST["publish_date"])
                new_post.save()
                return redirect('blog_view')
    else:
        form = CreatePostForm()
        return render(request, 'main/post.html', {'form' : form})

