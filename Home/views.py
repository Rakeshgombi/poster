from django.core.checks import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from Home.models import Contact, Profile
from Blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
import random
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
    context = {'allposts': allPosts, 'query': query}
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
            messages.warning(
                request, "Your query has been submitted successfully!")
            contact.save()
    return render(request, 'home/contact.html')


def userSettings(request, slug):
    username = get_object_or_404(User, username=slug)
    user = User.objects.filter(username=username).first()
    allPost = Post.objects.filter(author=username)
    profile = Profile.objects.filter(user=user).first()
    print(user)
    context = {"user": user, "profile": profile, "allPosts": allPost}
    if not(request.user.is_authenticated and request.user == username):
        return render(request, "home/userProfile.html", context)
    else:
        if request.method == "POST":
            dp = profile.display_pic
            try:
                print(request.FILES['display_pic'])
                profile.display_pic = request.FILES['display_pic']
                fs = FileSystemStorage(f'/media/pic_folder')
                fs.save(profile.display_pic.name, profile.display_pic)
            except Exception as e:
                print(e)
                profile.display_pic = dp 
            user.first_name = request.POST.get('first_name' '')
            user.last_name = request.POST.get('last_name' '')
            profile.organisation = request.POST.get('organisation' '')
            profile.country = request.POST.get('country' '')
            profile.website = request.POST.get('website' '')
            profile.facebook = request.POST.get('facebook' '')
            profile.instagram = request.POST.get('instagram' '')
            profile.github = request.POST.get('github' '')
            profile.twitter = request.POST.get('twitter' '')
            profile.bio = request.POST.get('bio' '')
            profile.save()
            user.save()
            print(request.POST.get('country', ''))
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return render(request, "home/userSettings.html", context)


def deleteProfilePicture(request):
    if request.method == 'POST':
        user = request.POST['profile']
        user = User.objects.filter(username=user).first()
        profile = Profile.objects.filter(user=user).first()
        print(profile.display_pic.delete())
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


email = ""
sentOtp = ""


def sendOtp(request):
    if request.method == "POST":
        global email
        email = request.POST.get('email', "")
        global sentOtp
        sentOtp = ""
        for i in range(6):
            sentOtp += str(random.randrange(0, 10))
        print(sentOtp)

        subject, from_email, to = f"Otp for your Blogging account at Poster", 'rakeshgombi18@gmail.com', f'{email}'
        text_content = f'Your OTP for email verification at Poster is <strong>{sentOtp}'
        html_content = f''' <div style="background: #eee; padding: 15px; margin: 0; display: inline-block; border-radius:10px ">
                    <div class="container"
                    style="padding: 10px; border-radius: 10px; background-color: rgb(255, 255, 255); display: inline-block; margin:0 auto">
                    <h4>Hi There,</h4>
                    <p>Your OTP for email verification at Poster is <strong>{sentOtp} </strong></p>
                    <p>Good luck! Have a nice day😊</p>
                    </div>
                    <p style="text-align: center; color: rgb(93, 93, 93);">Thank you for blogging with poster</p>
                    </div>'''
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return redirect("/")


def handleSignUp(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        global email
        global sentOtp
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        otp = request.POST['otp']
        if otp == sentOtp:
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
                    user = authenticate(username=username, password=pass1)
                    if user is not None:
                        login(request, user)
                    user.save()
                    profile = Profile(user=user)
                    profile.save()
                    messages.success(
                        request, 'Congratulations😊 Account created Successfully!')
            else:
                messages.warning(
                    request, 'Sorry😌, Passwords do not match! Try again')
        else:
            messages.warning(request, "OTP Does'nt match")
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
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
