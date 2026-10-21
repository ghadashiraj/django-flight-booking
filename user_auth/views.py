from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        au=authenticate(username=username,password=password)
        if au is not None:
            login(request,au)
            if request.user.is_authenticated:
                return redirect('home')
        else:
            return render(request,'login.html',{'wLogin':True})
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']

# !THIS TRY CATCH IS ADDED FOR IDENTIFY SAME USERNAME ENTERED

        try:
            ex=User.objects.get(username=username)
            return render(request,'register.html',{'wUname':True})
        
        except:

            u=User.objects.create(first_name=first_name,last_name=last_name,email=email,username=username)
            u.set_password(password)
            u.save()
            return redirect('login')
    return render(request,'register.html')

def logout_(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')

@login_required(login_url='login')
def upProf(request):
    od=User.objects.get(username=request.user)

    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']

        od.first_name=first_name
        od.last_name=last_name
        od.email=email
        od.username=username
        od.save()
        return redirect('profile')

    return render(request,'upProf.html',{'od':od})

@login_required(login_url='login')
def resPass(request):
    op=User.objects.get(username=request.user)
    if request.method == 'POST':
        try:
            oldPass=request.POST['oldPass']
            oc=authenticate(username=request.user,password=oldPass)
            # ^1ST METHOD
            # if oc is not None:
            #     return render(request,'resPass.html',{'done':True})
            # else:
            #     return render(request,'resPass.html',{'ErrorPass':True})

            # ^2ND METHOD
            if oc:
                return render(request,'resPass.html',{'done':True})
            else:
                return render(request,'resPass.html',{'ErrorPass':True})
        
        except:
            newPass=request.POST['newPass']
            confnewPass=request.POST['confnewPass']
            if newPass == confnewPass:
                op.set_password(newPass)
                op.save()
                logout(request)
                return redirect('login')
            else:
                return render(request,'resPass.html',{'done':True,'cErrorPass':True})
    return render(request,'resPass.html') 

