import socket

from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import dateformat

from Blog.models import Comment, Post

from .forms import CommentForm

# Create your views here.


def blogHome(request):

    allPost = Post.objects.all()
    context = {"allPosts": allPost}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    # get post object
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    author = User.objects.filter(username=post.author).first()
    print(author.email)
    # list of active parent comments
    comments = post.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                reply = post.comments.filter(
                    id=parent_id, active=True, parent__isnull=False)
                print(reply)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post = post
            # save
            new_comment.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/blogPost.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'author': author
                   })


def composeBlog(request):
    if request.method == 'POST':
        content = request.POST.get('content', "")
        if len(content) > 30:
            category = request.POST.get('category', "")
            title = request.POST.get('title', "")
            author = request.POST.get('author', "")
            post = Post(category=category, title=title,
                        author=author, content=content)
            post.save()
            analyzed = ""
            punctuations = """.,;:?!-()[]{}"'/@&-*^%<>#_$+="""
            for char in title:
                if char not in punctuations:
                    analyzed += char
            title = analyzed
            post.slug = str(post.sno) + "-" + title.replace(" ", "-")
            post.save()
        else:
            messages.info(request, "The content of the blog was Very less to post a blog")

    return render(request, 'blog/composeBlog.html')


def editPost(request, slug, owner):
    username = get_object_or_404(User, username=owner)
    user = request.user
    if username == user and request.user.is_authenticated:
        post = get_object_or_404(Post, slug=slug)
        context = {"post": post}
        if request.method == 'POST':
            content = request.POST.get('content', "")
            if len(content) > 30:
                category = request.POST['category']
                title = request.POST['title']
                analyzed = ""
                post.category = category
                post.title = title
                post.content = content
                post.save()
                punctuations = """.,;:?!-()[]{}"'/@&-*^%<>#_$+="""
                for char in title:
                    if char not in punctuations:
                        analyzed += char
                        title = analyzed
                post.slug = str(post.sno) + "-" + title.replace(" ", "-")
                post.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                messages.info(request, "The content of the blog was Very less to post a blog")
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return render(request, "blog/editPost.html", context)
    else:
        messages.warning(request, 'You are not authorised to visit this page')
        return redirect('/')


def deletePost(request):
    if request.method == "POST":
        slug = request.POST['slug']
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        print("deleted")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
