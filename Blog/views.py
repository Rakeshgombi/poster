import socket

from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import dateformat
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import FileSystemStorage
from Blog.models import Comment, Post
import os
from .forms import CommentForm

# Create your views here.


def blogHome(request):
    users = User.objects.all()
    allPost = Post.objects.all()
    categories = Post.objects.values('category').distinct()
    context = {"allPosts": allPost, "categories":categories, "users": users}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    author = User.objects.filter(username=post.author).first()
    print(author.email)
    comments = post.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                reply = post.comments.filter(
                    id=parent_id, active=True, parent__isnull=False)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            messages.success(request, "Your Comment has been posted")
            subject, from_email, to = f"New comment on your post {post.title}", 'rakeshgombi18@gmail.com', f'{author.email}'
            text_content = 'This is an important message.'
            html_content = f'''
             <div style="background: #eee; padding: 15px; margin: 0; display: inline-block; border-radius:10px ">
              <div class="container"
                style="padding: 10px; border-radius: 10px; background-color: rgb(255, 255, 255); display: inline-block; margin:0 auto">
                <h4>Hi {author.first_name} {author.last_name},</h4>
                <p><strong>{request.POST['name']}</strong> has just now commeted as <b>{request.POST['body']} </b> On your post
                  <strong>{post.title}</strong>
                </p>
                <p style="text-align: center;"><a href="http://127.0.0.1:8000/blog/61-Blog-Home/"
                    style="padding: 5px 10px; background: #ff7300; color: white; text-decoration: none; border-radius: 15px; display: inline-block; margin: 0 auto; text-align: center; font-size: large;"
                    target="_blank">Click to view</a></p>
                <p>Good luck! Have a nice day😊</p>
              </div>
              <p style="text-align: center; color: rgb(93, 93, 93);">Thank you for blogging with poster</p>
            </div>
            '''
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
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
    categories = Post.objects.values('category').distinct()
    print(categories)
    if request.method == 'POST':
        content = request.POST.get('content', "")
        if len(content) > 30:
            category = request.POST.get('category', "")
            title = request.POST.get('title', "")
            subtitle = request.POST.get('subtitle', "")
            author = request.POST.get('author', "")
            # print(request.FILES['thumbnail'])
            try:
                thumbnail = request.FILES['thumbnail']
                fs = FileSystemStorage('/media/blogThumbs')
                fs.save(thumbnail.name, thumbnail)
                print(request.FILES['thumbnail'])
            except Exception as e:
                # print(e)
                thumbnail = ""
            post = Post(category=category, title=title,
                        author=author, content=content, thumbnail=thumbnail, subtitle=subtitle)
            post.save()
            analyzed = ""
            punctuations = """.,;:?!-()[]{}"'/@&-*^%<>#_$+="""
            for char in title:
                if char not in punctuations:
                    analyzed += char
            title = analyzed
            post.slug = str(post.sno) + "-" + title.replace(" ", "-")
            post.save()
            
            messages.info(
                request, "Your Blog has been posted succefully")
        else:
            messages.info(
                request, "The content of the blog was Very less to post a blog")

    return render(request, 'blog/composeBlog.html', {'categories':categories})


def editPost(request, slug, owner):
    username = get_object_or_404(User, username=owner)
    user = request.user
    if username == user and request.user.is_authenticated:
        post = get_object_or_404(Post, slug=slug)
        context = {"post": post}
        if request.method == 'POST':
            content = request.POST.get('content', "")
            if len(content) > 30:
                category = request.POST.get('category', "")
                title = request.POST.get('title', "")
                subtitle = request.POST.get('subtitle', "")
                post.category = category
                post.title = title
                post.subtitle = subtitle
                post.content = content
                thumb = post.thumbnail
                try:
                    post.thumbnail = request.FILES['thumbnail']
                    fs = FileSystemStorage('/media/blogThumbs')
                    fs.save(post.thumbnail.name, post.thumbnail)
                    # print(request.FILES['thumbnail'])
                except Exception as e:
                    print(e)
                    post.thumbnail = thumb
                post.save()
                analyzed = ""
                punctuations = """.,;:?!-()[]{}"'/@&-*^%<>#_$+="""
                for char in title:
                    if char not in punctuations:
                        analyzed += char
                        title = analyzed
                post.slug = str(post.sno) + "-" + title.replace(" ", "-")
                post.save()
                messages.info(request, "Your Blog has been posted succefully")
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                messages.info(
                    request, "The content of the blog was Very less to post a blog")
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
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
