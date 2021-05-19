from django.core.checks import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from Home.models import Contact, Profile
from Blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import itertools 
# Create your views here.


def index(request):
    allPost = Post.objects.all().order_by('-views')[:10:1]
    context = {"allPosts": allPost}
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 70:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsAuthor, allPostsContent)
    context = {'allposts': allPosts, 'query':query}
    return render(request, 'home/search.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["query"]
        if len(name) < 2 or len(email) < 3 or len(content) < 4 or len(phone) < 10:
            messages.warning(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            messages.warning(request, "Your query has been submitted successfully!")
            contact.save()
    return render(request, 'home/contact.html')


def userProfile(request, slug):
    username = get_object_or_404(User, username=slug)
    user = User.objects.filter(username=username).first()
    allPost = Post.objects.filter(author=username)
    profile = Profile.objects.filter(user=user).first()
    context = {"user": user, "profile": profile, "allPosts": allPost}
    return render(request, 'home/userProfile.html', context)


def userSettings(request, slug):
    username = get_object_or_404(User, username=slug)
    user = User.objects.filter(username=username).first()
    allPost = Post.objects.filter(author=username)
    profile = Profile.objects.filter(user=user).first()
    context = {"user": user, "profile": profile, "allPosts": allPost}
    if request.method == "POST":
        if request.FILES['display_pic']:
            profile.display_pic = request.FILES['display_pic']
            fs = FileSystemStorage(f'/media/pic_folder/{request.user}')
            fs.save(profile.display_pic.name, profile.display_pic)
        if request.POST['first_name']:
            user.first_name = request.POST['first_name']
        if request.POST['last_name']:
            user.last_name = request.POST['last_name']
        if request.POST['organisaation']:
            profile.organisaation = request.POST['organisaation']
        if request.POST['country']:
            profile.country = request.POST['country']
        if request.POST['website']:
            profile.website = request.POST['website']
        if request.POST['facebook']:
            profile.facebook = request.POST['facebook']
        if request.POST['instagram']:
            profile.instagram = request.POST['instagram']
        if request.POST['github']:
            profile.github = request.POST['github']
        if request.POST['twitter']:
            profile.twitter = request.POST['twitter']
        if request.POST['bio']:
            profile.bio = request.POST['bio']
        profile.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    if request.user.is_authenticated and request.user == username:
        return render(request, 'home/usersettings.html', context)
    else:
        return render(request, 'home/userProfile.html', context)


def deleteProfilePicture(request):
    if request.method == 'POST':
        user = request.POST['profile']
        user = User.objects.filter(username=user).first()
        profile = Profile.objects.filter(user=user).first()
        print(profile.display_pic.delete())
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def handleSignUp(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            if len(pass1) < 8:
                messages.warning(
                    request, 'Sorry, Minimum length of the password must be 8')
            elif not(username.isalnum()):
                messages.warning(
                    request, 'Sorry, useranme can only be combinations of alphabets and numbers')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'Sorry, Username already taken')
            elif User.objects.filter(email=email).exists():
                messages.warning(
                    request, 'Sorry, Account with the same email already exists')
            else:
                user = User.objects.create_user(
                    first_name=fname, last_name=lname,  username=username, email=email, password=pass1)
                user.save()
                messages.success(
                    request, 'Congratulations😊 Account created Successfully!')
        else:
            messages.warning(
                request, 'Sorry😌, Passwords do not match! Try again')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponse("404 Error")


def handleSignIn(request):
    if request.method == "POST":
        loginusername = request.POST["loginusername"]
        loginPassword = request.POST["loginPassword"]
        user = authenticate(username=loginusername, password=loginPassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
        else:
            messages.error(request, "Invalid credentials! Please try again")

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponse("404 Not Found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')
