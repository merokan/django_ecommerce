from django.shortcuts import render, HttpResponse, redirect 
from django.contrib import messages
from models import *
import bcrypt

def index(request):
    if 'id' in request.session:
        return redirect('/home')
    else:
        context = {
            "user" : User.objects.all()
        }
        return render(request, 'drinksrus/index.html', context)

def register(request):
    errors = User.objects.register(request.POST)
    if len(errors):
        for key, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name= request.POST['first_name'], last_name= request.POST['last_name'], email = request.POST['email'], password = hash1)
        request.session['id'] = user.id
        return redirect('/home')

def login(request):
    if request.method == "POST":
        userList=User.objects.filter(email=request.POST['email'])
        errors = User.objects.login(request.POST)
        if len(userList) > 0:
            print userList
            user = userList[0]
        else:
            messages.error(request, "Email or password incorrect")
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id'] = user.id
            return redirect('/home')
        else:
            messages.error(request, "Email or password incorrect")
            return redirect('/')
    else:
        return redirect('/')

def home(request):
    if not 'id' in request.session:
        return redirect('/')
    else:
        return render(request, 'drinksrus/home.html')

def logout(request):
    del request.session['id']
    return redirect('/')