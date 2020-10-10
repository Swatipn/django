from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.contrib import messages
from .models import Contact,BlogPosts
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage

# Create your views here.

def index(request):
    return render(request,'index.html')

def contact(request):
    if request.method == 'POST':
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phone=request.POST.get('num')
        description=request.POST.get('desc')
        contact_query=Contact(name=fullname,email=email,phone=phone,description=description)
        contact_query.save()
        from_email=settings.EMAIL_HOST_USER
        # email starts here
        # your mail starts here
        connection=mail.get_connection()
        connection.open()
        email_message=mail.EmailMessage(f'Website Email : {fullname}',f'Email From : {email}\nUser Query : {description}\nPhone No : {phone}',from_email,['swati1642021@gmail.com'],connection=connection)
        connection.send_messages([email_message])
        connection.close()
        messages.info(request,'Thanks for contacting Us!!')
        return redirect('/contact')
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')


def handleBlog(request):
    if not request.user.is_authenticated:
        messages.error(request,'Please login and Try again!!')
        return redirect('/login')
    posts=BlogPosts.objects.all()
    context={'posts': posts}
    return render(request,'handleBlog.html',context)

def services(request):
    return render(request,'services.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        num = request.POST['num']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1!=pass2:
            messages.error(request,'Password not matching!!')
            return redirect('/signup')
        
        try:
            if User.objects.get(username=username):
                messages.error(request,'Username is already taken')
                return redirect('/signup')
            elif User.objects.get(email=email):
                messages.error(request,'email is already taken try with other email')
                return redirect('/signup')
           
        except Exception as identifier:
            pass    
            myuser=User.objects.create_user(username,email,pass1)
            myuser.firstname=firstname
            myuser.lastname=lastname
            myuser.num=num
            myuser.save()
            messages.success(request,'Signup successfull!!')
            return redirect('/')
    return render(request,'auth/signup.html')
       
    
def handlelogin(request):
    if request.method == 'POST':
        handleusername = request.POST['username']
        handlepassword = request.POST['pass1']
        user=authenticate(username=handleusername,password=handlepassword)
        if user is not None:
            login(request,user)
            messages.info(request,'Welcome to My website')
            return redirect('/')
        else:
            messages.warning(request,"Invalid credentials")
            return redirect('/login')
    return render(request,'auth/login.html')   


def handlelogout(request):
    logout(request)
    messages.success(request,'log out successful')
    return redirect('/login')
    
def addpost(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        content=request.POST.get('desc')
        name=request.POST.get('name')
        files=request.POST.FILES('file')
        query = BlogPosts(title=title,content=content,author=name,img=files)
        query.save()
        messages.info(request,'Your Post has been saved successfully!!!')
        return redirect('/handleBlog')

    return render(request,'addpost.html')